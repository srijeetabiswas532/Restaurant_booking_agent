from typing import Callable, Any # type hint helpers
from pydantic import BaseModel
from langchain.agents import Tool
import requests

# class ReservationInput(BaseModel):
#     name: str
#     date: str
#     time: str
#     party_size: int

def book_reservation(input: str) -> str:
    """
    Parses a flat input string and sends it to the mock API.
    Assumes input string contains 'name=', 'date=', 'time=', 'party_size='
    """

    # Simple parsing
    fields = dict(item.strip().split("=") for item in input.split(","))
    payload = {
        "name": fields["name"],
        "date": fields["date"],
        "time": fields["time"],
        "party_size": int(fields["party_size"]),
    }

    try:
        res = requests.post("http://localhost:8000/book", json=payload)
        res.raise_for_status()
        data = res.json()
        return f"{data['message']}\nDetails: {data['details']}"
    except Exception as e:
        return f"❌ Failed to book reservation: {str(e)}"


# Tool Definition (structured)

# book_reservation_tool = Tool.from_function(
#     func=book_reservation,
#     name='book_reservation',
#     description="""
#         Use this tool to book a restaurant reservation. 
#         Requires: name of restaurant, number of people, date (YYYY-MM-DD), and time (12-hour format with am/pm).
#     """,
#     args_schema=ReservationInput
# )

book_reservation_tool = Tool(
    name="book_reservation",
    func=book_reservation,
    description="""
        Use this tool to book a restaurant reservation. 
        Include the restaurant name, number of people, time (with am/pm), and date (e.g., 'today', 'tomorrow', or YYYY-MM-DD).
        If any of these are missing, ask the user to provide them.
    """
)
