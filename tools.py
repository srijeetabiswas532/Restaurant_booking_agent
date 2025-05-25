from typing import Callable, Any
from pydantic import BaseModel
from langchain.tools import StructuredTool
import requests

class CheckAvailabilityInput(BaseModel):
    name: str
    date: str
    time: str
    party_size: int

def check_availability_tool_fn(name: str, date: str, time: str, party_size: int) -> str:
    payload = {
        "name": name,
        "date": date,
        "time": time,
        "party_size": party_size
    }

    try:
        res = requests.post("http://localhost:8000/check", json=payload)
        res.raise_for_status()
        data = res.json()
        return data["message"]
    except Exception as e:
        return f"❌ Failed to check availability: {str(e)}"

check_availability_tool = StructuredTool.from_function(
    func=check_availability_tool_fn,
    name="check_availability",
    description="""
        Use this tool to check whether a reservation is available before booking.
        Requires the restaurant name, date, time (e.g. '7pm'), and number of people.
    """,
    args_schema=CheckAvailabilityInput
)

# ✅ Structured input schema for book_reservation
class ReservationInput(BaseModel):
    name: str
    date: str
    time: str
    party_size: int

def book_reservation_tool_fn(name: str, date: str, time: str, party_size: int) -> str:
    payload = {
        "name": name,
        "date": date,
        "time": time,
        "party_size": party_size,
    }

    try:
        res = requests.post("http://localhost:8000/book", json=payload)
        res.raise_for_status()
        data = res.json()
        return f"{data['message']}\nDetails: {data['details']}"
    except Exception as e:
        return f"❌ Failed to book reservation: {str(e)}"

book_reservation_tool = StructuredTool.from_function(
    func=book_reservation_tool_fn,
    name="book_reservation",
    description="""
        Use this tool to book a restaurant reservation.
        ONLY use this tool when you ALREADY know the restaurant name, party size, date (e.g. 'tomorrow'), and time (e.g. '7pm').
    """,
    args_schema=ReservationInput
)