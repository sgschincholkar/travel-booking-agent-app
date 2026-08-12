import datetime

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from backend.state import AgentState
from backend.tools import TOOLS

CURRENT_YEAR = datetime.datetime.now().year

TOOLS_SYSTEM_PROMPT = f"""You are a smart travel agency. Use the tools to look up information.
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
The current year is {CURRENT_YEAR}. If you don't get flights, try searching till you find them!
If you need to look up some information before asking a follow up question, you are allowed to do that!
In your output, include links to hotel websites and flight websites (if possible),
the logo of the hotel and the logo of the airline company (if possible),
and always include both the price of the flight and the price of the hotel (with currency).
For example, for hotels:
    Rate: $581 per night
    Total: $3,488
"""


class Agent:
    def __init__(self):
        self._tools = {t.name: t for t in TOOLS}
        self._tools_llm = ChatAnthropic(model="claude-sonnet-5").bind_tools(TOOLS)

        builder = StateGraph(AgentState)
        builder.add_node("call_tools_llm", self.call_tools_llm)
        builder.add_node("invoke_tools", self.invoke_tools)
        builder.add_node("email_sender", self.email_sender)
        builder.set_entry_point("call_tools_llm")

        builder.add_conditional_edges(
            "call_tools_llm",
            Agent.exists_action,
            {"more_tools": "invoke_tools", "email_sender": "email_sender"},
        )
        builder.add_edge("invoke_tools", "call_tools_llm")
        builder.add_edge("email_sender", END)

        memory = MemorySaver()
        self.graph = builder.compile(checkpointer=memory, interrupt_before=["email_sender"])

    @staticmethod
    def exists_action(state: AgentState):
        result = state["messages"][-1]
        if len(result.tool_calls) == 0:
            return "email_sender"
        return "more_tools"

    def call_tools_llm(self, state: AgentState):
        messages = state["messages"]
        messages = [SystemMessage(content=TOOLS_SYSTEM_PROMPT)] + [
            self._strip_thinking(m) for m in messages
        ]
        message = self._tools_llm.invoke(messages)
        return {"messages": [message]}

    @staticmethod
    def _strip_thinking(message: AnyMessage) -> AnyMessage:
        if not isinstance(message.content, list):
            return message
        filtered = [
            block
            for block in message.content
            if not (isinstance(block, dict) and block.get("type") == "thinking")
        ]
        if filtered == message.content:
            return message
        return message.copy(update={"content": filtered})

    def invoke_tools(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            if t["name"] not in self._tools:
                results.append(
                    ToolMessage(tool_call_id=t["id"], name=t["name"], content="Bad tool name")
                )
            else:
                result = self._tools[t["name"]].invoke(t["args"])
                results.append(
                    ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
                )
        return {"messages": results}

    def email_sender(self, state: AgentState):
        return {"messages": []}
