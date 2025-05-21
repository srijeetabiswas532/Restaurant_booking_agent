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
    """Use this tool to book a reservation. 
    Only call this tool when you know: name of the restaurant, number of people, date (e.g. 'tomorrow'), and time (e.g. '7pm'). Otherwise do NOT use this tool yet, ask the user for more complete information before using this tool or else it will throw an error.
    Format input like: name:Jet B, date:tomorrow, time:7pm, party_size:2    
    """
    if ":" not in input:
        return f"❌ Tool input was not in expected format. Got: {input}"
    
    if "name:" not in input.lower() or "date:" not in input.lower() or "time:" not in input.lower() or "size:" not in input.lower():
        return f"❌ Tool input was not in expected format. Got: {input}. Format input like: name:Jet B, date:tomorrow, time:7pm, party_size:2"
    
    # Simple parsing
    fields = dict(item.strip().split(":") for item in input.split(","))
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
