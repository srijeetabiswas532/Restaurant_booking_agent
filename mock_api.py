from fastapi import FastAPI
from pydantic import BaseModel

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
    return {
        "message": "Reservation confirmed ✅",
        "details": {
            "name": reservation.name,
            "date": reservation.date,
            "time": reservation.time,
            "party_size": reservation.party_size
        }
    }