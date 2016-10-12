from flask import Flask, request, redirect
import twilio.twiml

# For TESTing -- START
from twilio.rest import TwilioRestClient
# For TESTing -- END

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    msg = "Hello, this is your assistant. :) Let's begin!"
    resp.message(msg)

    # For TESTing -- START
    # Find these values at https://twilio.com/user/account
    account_sid = "ACe9748f2bce3601801167fa0791836c3e"
    auth_token = "cef3bac7ba6d045c7e6cf4b6c21581eb"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+919591361570", from_="+18779545971",
                                         body=msg)
    # For TESTing -- END


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
