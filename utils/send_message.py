import os
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
number = os.getenv("TWILIO_NUMBER")


def send_message(body, to):
    message = client.messages \
                    .create(
                        body=body,
                        from_=number,
                        to=to
                    )

    return message.sid