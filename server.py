from flask import Flask, request, redirect
import twilio.twiml
import random
import requests

# For TESTing -- START
from twilio.rest import TwilioRestClient
# For TESTing -- END

app = Flask(__name__)

# For TESTing -- START
def send_sms_to_jitesh(message):
    # Credentials owner: jiteshjha96@gmail.com
    # Find these values at https://twilio.com/user/account
    account_sid = "ACe9748f2bce3601801167fa0791836c3e"
    auth_token = "cef3bac7ba6d045c7e6cf4b6c21581eb"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+919591361570", from_="+18779545971",
                                         body=message)
# For TESTing -- END



# @app.route("/sms", methods=['GET', 'POST'])
# def sms():
#     """Respond to incoming calls with a simple text message."""
#
#     resp = twilio.twiml.Response()
#     message_body = request.values.get('Body', None)
#
#     # Remove annoying text prefix announcing trial version
#     prefix = "Sent from your Twilio trial account - "
#     message_body = message_body[len(prefix):]
#     message = "Hello, this is your assistant. :) Let's begin!" + " Body:" + message_body
#
#     resp.message(message)
#
#     # For TESTing -- START
#     send_sms_to_jitesh(message)
#     # For TESTing -- END
#
#     # Return the message to Twilio (or send out the message)
#     return str(resp)

noIntent = [
    "I'm having trouble understanding you, could you rephrase your question?",
    "I didn't catch that, could you rephrase your query?",
    "Sorry, I didn't understand that. Try rephrasing your request."
]

@app.route("/no_intent", methods=['POST'])
def no_intent():
    resp = twilio.twiml.Response()
    message = random.choice(noIntent)
    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/weather", methods=['POST'])
def weather(entities):
    resp = twilio.twiml.Response()
    message = entities['location'][0]['value']
    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp


@app.route("/sms", methods=['GET', 'POST'])
def sms():
    message_body = request.values.get('Body', None)

    # Remove annoying text prefix announcing trial version
    prefix = "Sent from your Twilio trial account - "
    message_body = message_body[len(prefix):]

    response = requests.get(url='https://api.wit.ai/message?v=20161022&q='+message_body,headers={'Authorization': 'Bearer TUDKLORVVMITDT4FCJFMAARQAWB2NLJ2'})
    dict_response = json.loads(response.text)

    intent = None
    confidence = None
    entities = None
    msg = None

    if dict_response['entities']['intent']:
        intent = dict_response['entities']['intent'][0]['value']
        confidence = dict_response['entities']['intent'][0]['confidence']
        entities = dict_response['entities']

    if intent is None or confidence < 0.2:
        msg = no_intent()
    elif intent == "weather":
        msg = weather(entities)
    else:
        msg = "Feature not supported"

    return str(msg)

if __name__ == "__main__":
    app.run(debug=True)
