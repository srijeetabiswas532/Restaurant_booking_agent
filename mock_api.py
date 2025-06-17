import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import json

load_dotenv()
app = FastAPI()

class Reservation(BaseModel):
    name: str
    date: str
    time: str
    party_size: int
    email: str

def send_confirmation_email(reservation: Reservation):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = reservation.email

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📅 Your Restaurant Reservation is Confirmed!"
    msg["From"] = sender
    msg["To"] = recipient

    html = f"""
    <html>
    <body>
        <h2>📅 Reservation Confirmation</h2>
        <p>Hi there! Your reservation has been successfully confirmed.</p>
        <ul>
            <li><strong>Restaurant:</strong> {reservation.name}</li>
            <li><strong>Date:</strong> {reservation.date}</li>
            <li><strong>Time:</strong> {reservation.time}</li>
            <li><strong>Party Size:</strong> {reservation.party_size}</li>
        </ul>
        <p>Thanks for using our service!</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("📧 Email sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# defines an API endpoint ("/book")
# accepts a JSON body that matches Reservation pydantic model
@app.post("/book")
def book(reservation: Reservation):
    with open("bookings.json", "a") as f:
        json.dump(reservation.dict(), f)
        f.write("\n")

    send_confirmation_email(reservation)

    return {
        "message": "Reservation confirmed ✅",
        "details": reservation.dict()
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
