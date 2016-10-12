# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "ACe464c41a9b742a67a494ae0b08fd6a7c"
auth_token = "8473ba13daed9e9f7a3d8fe2cb20941d"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+18779545971", from_="+12024992521",
                                     body="Hello there!")
print message
