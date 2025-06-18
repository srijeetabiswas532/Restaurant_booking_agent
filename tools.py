from typing import Callable, Any, Optional
from pydantic import BaseModel
from langchain.tools import StructuredTool
import requests
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory


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
        Use this tool to check availability for a restaurant before booking the restaurant.
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
    email: Optional[str] = None  # ✅ optional with default

# Wrap the booking function to inject email before calling the real function
def wrapped_book_reservation_tool_fn(name: str, date: str, time: str, party_size: int, email: Optional[str] = None) -> str:
    from streamlit import session_state
    email = session_state.get("user_email", "")
    return book_reservation_tool_fn(name, date, time, party_size, email)


def book_reservation_tool_fn(name: str, date: str, time: str, party_size: int, email: str) -> str:
    payload = {
        "name": name,
        "date": date,
        "time": time,
        "party_size": party_size,
        "email": email
    }
    try:
        res = requests.post("http://localhost:8000/book", json=payload)
        res.raise_for_status()
        data = res.json()
        return f"{data['message']}\nDetails: {data['details']}"
    except Exception as e:
        return f"❌ Failed to book reservation: {str(e)}"

book_reservation_tool = StructuredTool.from_function(
    func=wrapped_book_reservation_tool_fn,
    name="book_reservation",
    description="""
        Use this tool to book a restaurant reservation.
        ONLY use this tool when you ALREADY know the restaurant name, party size, date (e.g. 'tomorrow'), and time (e.g. '7pm').
    """,
    args_schema=ReservationInput
)


# creating a class and function to search YELP using API for restaurants
class RestaurantSearchInput(BaseModel):
    location: str
    term: str

def search_restaurants_fn(term: str, location: str) -> str:
    load_dotenv()
    api_key = os.getenv("YELP_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"term": term, "location": location, "limit": 5}

    try:
        res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
        res.raise_for_status()
        data = res.json()
        businesses = data.get("businesses", [])

        if not businesses:
            return "No restaurants found for your search"
        
        # response = "Top restaurants found:\n"
        # top_restaurant = businesses[0]["name"]
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # memory.chat_memory.add_ai_message(f"Great, I will use {top_restaurant} for future steps, like for the restaurant_name.")
        return businesses
    
    except Exception as e:
        return f"Failed to search restaurants: {str(e)}"
    
search_restaurant_tool = StructuredTool.from_function(
    func=search_restaurants_fn,
    name='search_restaurants',
    description="Use this tool to search for real restaurants by cuisine, keyword, or name and location using Yelp.",
    args_schema=RestaurantSearchInput
)
