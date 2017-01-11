# hello_friend

Code.Fun.Do 2016 Hackathon project by team ./ [dot slash]

A Q&A service through SMS.

Number: +1 206-745-6187

## Features
* Call for help using the SOS module
* Find the best route to your destination
* Catch up on the latest news
* Find out meaning for a new word
* Find your nearest ATM
* In a foreign country? Use Translate to speak the native language
* Keep up with the stock market
* Check out information on all the movies
* Prepare for sun or rain with weather updates

And the best part? No need to have Internet, or even a smartphone.


## APIs used
* [Twilio](https://www.twilio.com)
* [Heroku](https://www.heroku.com)
* [Wit.ai](https://wit.ai)
* [Bing Maps API](https://www.microsoft.com/maps/choose-your-bing-maps-API.aspx)
* [Google Places API](https://developers.google.com/places/)
* [Bing Translate API](https://www.microsoft.com/en-us/translator/translatorapi.aspx)
* [Open Weather Map API](https://openweathermap.org/api)
* [Bing News API](http://www.bing.com/developers/s/APIBasics.html)
* [OMDB API](https://www.omdbapi.com)
* [Duck Duck Go Instant Answer API](https://duckduckgo.com/api)
* [Yahoo Finance](https://pypi.python.org/pypi/yahoo-finance/1.1.4)


## Developed by

[Yash Kumar Lal](https://github.com/ykl7)

[Jitesh Kumar Jha](https://github.com/jiteshjha)

[Avikant Saini](https://github.com/avikantz)


## Beta Testing

Since a trial Twilio account (valid for 30 days (expires on Feb 8, 2017)) has been used, the number (user) used to send and receive messages and information needs to be verified on Twilio through the account that has been used in setup of the service. Please contact any of the 3 of use for the same.

The information being received is also dependent on the APIs being used, which have been listed above. Sometimes, the response returned is slow, so patience is advised, or the request might also return invalid messages.

### Templates

To test out various modules, templates can be found below:
* ```navigate from locality, city to locality, city```. To and from locations can be interchanged as well. The correct interpretation is autodetected.
* ```whats the weather in city today```
* ```help locality, city``` OR ```sos locality, city```
* ```how do you say word in language```
* ```imdb movie-name```
* ```stocks stock-name```
* ```atm near locality, city```
* ```define word/phrase```
* ```show me sports news```

### Languages

The languages currently supported by our Translate feature are:

* German
* French
* Spanish
* Chinese