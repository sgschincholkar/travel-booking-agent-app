import os
import traceback
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from backend.agent import Agent
from backend.email_sender import send_html_email


agent = Agent()


def extract_text(message) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text") or "")
        return "".join(parts)
    return str(content)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    thread_id: str
    response: str


class EmailRequest(BaseModel):
    thread_id: str
    sender: str
    receiver: str
    subject: str


class EmailResponse(BaseModel):
    status: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Backend started")
    yield
    print("Backend shutdown")


app = FastAPI(title="Travel Booking Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Process travel query through agent and return results.
    """
    try:
        thread_id = str(uuid.uuid4())
        messages = [HumanMessage(content=request.query)]

        config = {"configurable": {"thread_id": thread_id}}
        state = agent.graph.invoke({"messages": messages}, config=config)

        last_message = state["messages"][-1]
        response_text = extract_text(last_message)

        return QueryResponse(thread_id=thread_id, response=response_text)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/send-email", response_model=EmailResponse)
def send_email(request: EmailRequest):
    """
    Send travel results via email.
    """
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        state = agent.graph.invoke({}, config=config)

        last_message = state["messages"][-1]
        travel_html = extract_text(last_message)

        result = send_html_email(
            travel_html=travel_html,
            sender=request.sender,
            receiver=request.receiver,
            subject=request.subject
        )

        return EmailResponse(status=result)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
