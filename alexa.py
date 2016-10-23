#!/usr/bin/env python
import requests
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
#from datetime import datetime



app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
    print("entered in webhook")
    req = request.get_json(silent=True, force=True)  # parse request

    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)


    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    '''
    called by webhook.
    :param req:
    :return:
    '''

    # if the action if "phonenumber" we must see if it is a valid number
    if req.get("request").get("type") == "IntentRequest":

        if req.get("request").get("intent").get("name") == "Welcome" :

            session_attributes = req.get("session").get("attributes")
            should_end_session = False
            card_title = "Horoscope"
            speech_output = "Welcome to Horoscope trivia skill. let's Begin by saying your Horoscope Sign"

            reprompt_text = "Welcome to Horoscope trivia skill. let's Begin by saying your Horoscope Sign"


        if req.get("request").get("intent").get("name") == "HoroscopeIntent" :

            session_attributes = req.get("session").get("attributes")
            should_end_session = False
            card_title = "Horoscope"

            intent = req.get("request").get("intent")

            print intent

            sign = intent['slots']['Sign']['value']

            if 'value' in intent['slots']['Date']:

                day = intent['slots']['Date']['value']
            else:

                day = 'today'

            print sign

            url = 'http://horoscope-api.herokuapp.com/horoscope/' + day + '/' + sign

            print url
            
            headers = {'Content-Type': 'application/json' }
            seeitresult = requests.get(url, headers=headers)

            print seeitresult

            tvshowoutput = seeitresult.json() 

            print tvshowoutput

            speech_output = "%s" %tvshowoutput['horoscope']
            reprompt_text = "%s" %tvshowoutput['horoscope']


        if req.get("request").get("intent").get("name") == "Goodbye" :

            session_attributes = req.get("session").get("attributes")
            should_end_session = True
            card_title = "Horoscope"
            speech_output = "thank you  for choosing Horoscope trivia skill. Goodbye"

            reprompt_text = "thank you for choosing Horoscope trivia skill. Goodbye"

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
