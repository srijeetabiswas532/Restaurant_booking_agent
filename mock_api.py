from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Reservation(BaseModel):
    name: str
    date: str
    time: str
    party_size: int

# defines an API endpoint ("/book")
# accepts a JSON body that matches Reservation pydantic model
@app.post("/book")
def book(reservation: Reservation):
    # logging a JSON file with inputs
    with open("bookings.json", "a") as f:
        json.dump(reservation.dict(), f)
        f.write("\n")
    return {
        "message": "Reservation confirmed ✅",
        "details": {
            "name": reservation.name,
            "date": reservation.date,
            "time": reservation.time,
            "party_size": reservation.party_size
        }
    }

@app.post("/check")
def check(reservation: Reservation):
    # Very basic fake logic: everything is "available" unless it's at "midnight" Need to replace later.
    if reservation.time.lower() == "12am" or reservation.time.lower() == "midnight":
        return {
            "available": False,
            "message": f"No availability at {reservation.time} for {reservation.name}. Ask the user for another time."
        }

    return {
        "available": True,
        "message": f"Table is available at {reservation.time} on {reservation.date} for {reservation.party_size} people at {reservation.name}."
    }
