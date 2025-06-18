import smtplib
from email.message import EmailMessage
import traceback

sender = "jetb34632@gmail.com"
password = "gboo ehno xkhe gnxg"
recipient = "srijeetabiswas366@gmail.com"

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = sender
msg["To"] = recipient
msg.set_content("This is a test email from Python.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)

print("✅ Email sent!")
traceback.print_exc()