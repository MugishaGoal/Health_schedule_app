from flask import Flask, request
import africastalking
from twilio.rest import Client

app = Flask(__name__)

# Initialize Africa's Talking
username = "sandbox"
api_key = "atsk_6a0f26cd658383a33e6a2564b2e228d056f9a1cf81f6fb10e3fd2ffb2ecfa5d4f939a13a"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Initialize Twilio
account_sid = '.......'
auth_token = '.......'
twilio_client = Client(account_sid, auth_token)
twilio_phone_number = '.......'

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", None)

    if text == "":
        response = "CON Welcome to the Health Services\n"
        response += "1. Schedule Appointment\n"
        response += "2. Health Check Reminders"
    elif text == "1":
        response = "CON Enter your name:"
    elif text.startswith("1*"):
        details = text.split("*")
        if len(details) == 2:
            response = "CON Enter preferred date (DD-MM-YYYY):"
        elif len(details) == 3:
            response = "CON Enter preferred time (HH:MM):"
        elif len(details) == 4:
            response = "CON Enter health center:"
        elif len(details) == 5:
            response = "CON Enter medical option"
        elif len(details) == 6:
            name = details[1]
            date = details[2]
            time = details[3]
            health_center = details[5]
            medical_option = details[6]
            response = f"END Appointment scheduled for {name} on {date} at {time} at {health_center} in {medical_option}.\nYou will receive a reminder SMS."
            send_sms(phone_number, f"Appointment confirmed for {date} at {time} at {health_center} in {medical_option}.")
    elif text == "2":
        response = "CON Enter your name to subscribe for health check reminders:"

    elif text.startswith("2*"):
        details = text.split("*")
        if len(details) == 2:
            name = details[1]
            response = f"END Thank you {name}, you are now subscribed for health check reminders."
            send_sms(phone_number, "You are subscribed for health check reminders. Stay healthy!")
    else:
        response = "END Invalid option"

    return response

def send_sms(to, message):
    twilio_client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to
    )

if __name__ == '__main__':
    app.run(debug=True)
