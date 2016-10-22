#!/usr/bin/python

from flask import Flask, request, redirect
import twilio.twiml
import random
import requests
import json
from googleplaces import GooglePlaces, types, lang
from microsofttranslator import Translator

gp_api_key = 'AIzaSyAX_75N29J--rh3Qj9gXjMBVx9IuD_Um74'
google_places = GooglePlaces(gp_api_key)

bing_api_key = 'oeToVPEyRZIASRK2n2byOU1x0EMatLIpd8kCIvwXmMw'

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

@app.route("/sos", methods=["POST"])
def sos(dict_response):
    resp = twilio.twiml.Response()
    query_text = dict_response["_text"]

    # remove sos prefix and clean location string
    if query_text.find("sos ") != -1:
        query_text = query_text[4:]
    if query_text.find(" sos") != -1:
        query_text = query_text[:-4]
    if query_text.find("help ") != -1:
        query_text = query_text[5:]
    if query_text.find(" help") != -1:
        query_text = query_text[:-5]

    query_result = google_places.nearby_search(location=query_text, keyword='hospital', radius=5000, types=[types.TYPE_HOSPITAL])

    number_of_places = 0
    message = "List of Hospitals:\n"

    for place in query_result.places:
        if number_of_places < 3:
            number_of_places += 1
            message = message + place.name
            place_info = place.get_details()
            message = message + ", Ph: " + place.local_phone_number + "\n"
        else:
            break

    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/weather", methods=['POST'])
def weather(entities):
    resp = twilio.twiml.Response()
    location = entities['location'][0]['value']
    response = requests.get(url="http://api.openweathermap.org/data/2.5/weather?q=" + location + "&APPID=500d01a6ece6498b1cbf94ed23519119")
    dict_response = json.loads(response.text)

    temperature_in_celsius = round(dict_response['main']['temp'] - 273.15, 2)
    humidity = dict_response['main']['humidity']
    weather_description = dict_response['weather'][0]['description']

    message = "The weather in " + location + ": " + weather_description + ". "
    message += "The temperature is: " + str(temperature_in_celsius) + " C."
    message += "The humidity is: " + str(humidity) + " %."

    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/navigate", methods=['POST'])
def navigate(entities):
    resp = twilio.twiml.Response()
    destination = entities['to'][0]['value']
    origin = entities['from'][0]['value']

    key = "GSC5hkB0CEmUyk4nI2MY~HxNEzo1P1bHB1sX8EzDJpA~AmYeCHqvBerEI06DBSKWfo4pgB1w9Krgk7EH6lhGqqf3s5RaJArOzWJ-SL6AYVVw"
    bingMapsResponse = requests.get(url="http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + origin + "&wp.1=" + destination + "&avoid=minimizeTolls&key="+key)
    bingMaps_dict = json.loads(bingMapsResponse.text)
    resources = bingMaps_dict.get('resourceSets')[0].get('resources')
    routeLegs = resources[0].get('routeLegs')
    message = ""
    distance = routeLegs[0].get('routeSubLegs')[0].get('travelDistance')
    message += "Total Trip Distance: " + str(distance) + " km\n"
    duration = routeLegs[0].get('routeSubLegs')[0].get('travelDuration')
    message += "Total Trip Duration: " + str(duration/60) + " min \n"
    itineraryItems = routeLegs[0].get('itineraryItems')
    count = 1
    for item in itineraryItems:
        message += str(count) + ". " + item.get('instruction').get('text') + " ("
        message += str(item.get('travelDistance')) + " km, "
        message += str(item.get('travelDuration') / 60 ) + " min)"
        message += "\n"
        count +=1

    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/translate", methods=['POST'])
def translate(entities):
    resp = twilio.twiml.Response()

    message = ""

    text_for_translation = entities['phrase_to_translate'][0]['value']
    language =  entities['language'][0]['value'].lower()

    if language == "spanish":
        language = "es"
    elif language == "french":
        language = "fr"
    elif language == "german":
        language = "de"
    elif language == "chinese":
        language = "zh-CHS"
    else:
        message = "Language not supported!"

    if message != "Language not supported!":
        message = "Translation for " + text_for_translation + " to " + language + ":\n"
        translator = Translator('SMSAssistant', 'fhV+AdYFiK0QfQ4PFys+oQ/T0xiBBVQa32kxxbP55Ks=')
        message += translator.translate(text_for_translation, language)

    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/news", methods=['POST'])
def getNews(entities):
    resp = twilio.twiml.Response()
    newstopic = entities['news_topic'][0]['value']

    # default topic
    if newstopic is None:
        newstopic = "world"

    response = requests.get(url='https://api.datamarket.azure.com/Bing/Search/News?$format=json&Query=%27' + newstopic + "%27", \
     auth=(bing_api_key, bing_api_key))

    news_dict = json.loads(response.text)
    news = news_dict.get('d').get('results')

    message = ""

    if len(news) >= 5:
        message = "Here are the top 5 stories about " + newstopic + ":\n"
        for x in range(0, 5):
            message += str(x+1) + ". " + news[x].get('Title') + ".\n"
    else:
        message = "Here are the top news stories about " + newstopic + ":\n"
        for item in news:
            message += "- " + item.get('Title') + "\n"

    resp.message(message)

    # For TESTing -- START
    send_sms_to_jitesh(message)
    # For TESTing -- END

    return resp

@app.route("/define", methods=['POST'])
def define(entities):
    resp = twilio.twiml.Response()

    #topic = entities['wikipedia_search_query'][0]['value']

    # r = requests.get(url='http://api.duckduckgo.com/?q=' + topic + '&format=json&pretty=1')
    #
    # topic_response = json.loads(r.text)
    # all_definitions = topic_response['RelatedTopics']
    # top_definitions = all_definitions[0]
    # definition = top_definitions['Text']
    #
    # message = topic + " is defined as - " + definition

    resp.message(str(entities.get('wikipedia_search_query')))
    # print message

    # For TESTing -- START
    send_sms_to_jitesh(str(entities.get('wikipedia_search_query')))
    # For TESTing -- END

    return resp

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    message_body = request.values.get('Body', None)

    # Remove annoying text prefix announcing trial version
    prefix = "Sent from your Twilio trial account - "

    if prefix in message_body:
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
    elif intent == "navigate":
        msg = navigate(entities)
    elif intent == "sos":
        msg = sos(dict_response)
    elif intent == "translate":
        msg = translate(entities)
    elif intent == "news":
        msg = getNews(entities)
    elif intent == "define":
        msg = define(entities)
    else:
        msg = "Feature not supported"

    return str(msg)

if __name__ == "__main__":
    app.run(debug=True)
