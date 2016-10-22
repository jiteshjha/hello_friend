#!/usr/bin/python

import json
import omdb
import sys

def imdb(input_string):
	response = omdb.request(t='' + input_string + '', r='json'	)
	data = json.loads(response.text)
	# print data
	message = ""
	mediatype = data["Type"]
	year = data["Year"]
	title = data["Title"]
	if mediatype == "movie":
		message += "Found a Movie, \"" + title + "\" (" + year + ")\n"
	elif mediatype == "series":
		message += "Found a TV show, \"" + title + "\" (" + year + ")\n"
	for key in data:
		if key in ["Rated", "Runtime", "Genre", "Director", "Writer"]:
			if data[key] != "N/A":
				message += key + ": " + data[key] + "\n"
		if key == "imdbRating":
			message += "IMDB: " + data[key] + "\n"
	if data["Plot"] != "N/A":
		message += "Plot: " + data["Plot"]
	return message

try:
	name = sys.argv[1]
except:
	name = raw_input("Enter movie name: ")

print imdb(name)