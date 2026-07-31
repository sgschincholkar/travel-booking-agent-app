import os
from typing import Optional

import serpapi
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class FlightsInput(BaseModel):
    departure_airport: Optional[str] = Field(description="Departure airport code (IATA)")
    arrival_airport: Optional[str] = Field(description="Arrival airport code (IATA)")
    outbound_date: Optional[str] = Field(description="Outbound date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(description="Return date (YYYY-MM-DD)")
    adults: Optional[int] = Field(1, description="Number of adults (default 1)")
    children: Optional[int] = Field(0, description="Number of children (default 0)")
    infants_in_seat: Optional[int] = Field(0, description="Number of infants in seat (default 0)")
    infants_on_lap: Optional[int] = Field(0, description="Number of infants on lap (default 0)")


class FlightsInputSchema(BaseModel):
    params: FlightsInput


@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
    """
    Find flights using the Google Flights engine (via SerpAPI).
    Returns:
        dict or str: Flight search results or error message.
    """
    query = {
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": params.departure_airport,
        "arrival_id": params.arrival_airport,
        "outbound_date": params.outbound_date,
        "return_date": params.return_date,
        "currency": "USD",
        "adults": params.adults,
        "infants_in_seat": params.infants_in_seat,
        "stops": "1",
        "infants_on_lap": params.infants_on_lap,
        "children": params.children,
    }
    try:
        search = serpapi.search(query)
        return search.data["best_flights"]
    except Exception as e:
        return str(e)


class HotelsInput(BaseModel):
    q: str = Field(description='Location for hotels (e.g., "New York")')
    check_in_date: str = Field(description="Check-in date (YYYY-MM-DD)")
    check_out_date: str = Field(description="Check-out date (YYYY-MM-DD)")
    sort_by: Optional[str] = Field(8, description="Sorting parameter (default=8 for rating)")
    adults: Optional[int] = Field(1, description="Number of adults (default 1)")
    children: Optional[int] = Field(0, description="Number of children (default 0)")
    rooms: Optional[int] = Field(1, description="Number of rooms (default 1)")
    hotel_class: Optional[str] = Field(None, description='Filter by hotel class (e.g., "3" or "4")')


class HotelsInputSchema(BaseModel):
    params: HotelsInput


@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    """
    Find hotels using the Google Hotels engine (via SerpAPI).
    Returns:
        list or str: Up to 5 hotel property dicts or error message.
    """
    query = {
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "engine": "google_hotels",
        "hl": "en",
        "gl": "us",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "currency": "USD",
        "adults": params.adults,
        "children": params.children,
        "rooms": params.rooms,
        "sort_by": params.sort_by,
        "hotel_class": params.hotel_class,
    }
    try:
        search = serpapi.search(query)
        data = search.data
        return data["properties"][:5]
    except Exception as e:
        return str(e)


TOOLS = [flights_finder, hotels_finder]
