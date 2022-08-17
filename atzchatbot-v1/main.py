# coding:utf-8
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

# Messenger API integration example
# We assume you have:
# * a Wit.ai bot setup (https://wit.ai/docs/quickstart)
# * a Messenger Platform setup (https://developers.facebook.com/docs/messenger-platform/quickstart)
# You need to `pip install the following dependencies: requests, bottle.
#
# 1. pip install requests bottle
# 2. You can run this example on a cloud service provider like Heroku, Google Cloud Platform or AWS.
#    Note that webhooks must have a valid SSL certificate, signed by a certificate authority and won't work on your localhost.
# 3. Set your environment variables e.g. WIT_TOKEN=your_wit_token
#                                        FB_PAGE_TOKEN=your_page_token
#                                        FB_VERIFY_TOKEN=your_verify_token
# 4. Run your server e.g. python examples/messenger.py {PORT}
# 5. Subscribe your page to the Webhooks using verify_token and `https://<your_host>/webhook` as callback URL.
# 6. Talk to your bot on Messenger!

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
from types import SimpleNamespace

import requests
import urllib.parse
from bottle import Bottle, request, debug, static_file
from wit import Wit

# Wit.ai parameters
# WIT_TOKEN = os.environ.get('WIT_TOKEN')
# Messenger API parameters
# FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# A user secret to verify webhook get request.
# FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

WIT_TOKEN = "NUGVOTBUADICQ47GARTMSMAIKHM5F5IO"
FB_PAGE_TOKEN = "EAAEnIfhGYjcBANVJZAgSWgwDALfbKWrFFU0VKqTLRSgsIU14d9VnQfedyPITC1AZANJHnxjPBPdhK8oL2Qs3yQt8xgTli4ad3CfZCkHzmiVY4JrWj4qopcK93eXe5Q6Q8ZCnwKqPOo5O9gD3Q57vspiXbiWONL02dIl25xoD8VXID6x4sPbq"
FB_VERIFY_TOKEN = "ngrok.io"
DASHBOARD_URL = "https://atz-dashboard.herokuapp.com/content/tpl/"

# TRAITS_LIST = [
#                 'logoAtz', 'logoAtzAlt', 'listHarga',
#                 'hargaProduk', 'jenisSemuanya', 'jenisHmpk',
#                 'templateWeb'
#             ]

TRAITS_MAIN = ['hargaProduk', 'jenisSemuanya', 'jenisHmpk']
TRAITS_IMG = ['logoAtz', 'logoAtzAlt', 'listHarga']
TRAITS_VID = []
TRAITS_MEDIA = []
TRAITS_FILE = []
TRAITS_TEMPLATE = ['templateWeb', 'cpGiant01']

TRAITS_LIST = TRAITS_MAIN + TRAITS_IMG + TRAITS_VID + TRAITS_MEDIA + TRAITS_FILE + TRAITS_TEMPLATE

# Setup Bottle Server
debug(True)
app = Bottle()


# Facebook Messenger GET Webhook
@app.get('/webhook')
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.query.get('hub.verify_token')
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    print(str(data))
    if data['object'] == 'page':
        for entry in data['entry']:
            # get all the messages
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message['sender']['id']
                msg_text = message.get('message')
                if msg_text:
                    if message['message'].get('text'):
                        # We retrieve the message content
                        text = message['message']['text']
                        # Let's forward the message to Wit /message
                        # and customize our response to the message in handle_message
                        # response = client.message(msg=text, context={'session_id': fb_id})
                        response = client.message(msg=text)
                        print(str(response))
                        handle_message(response=response, fb_id=fb_id, msg=text)
    # else:
    # Returned another event(save to exceptions logger)
    # return 'Received Different Event'
    return None


@app.route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/assets')


def fb_message(sender_id, text, trait):
    """
    Function for returning response to messenger
    """
    traits_img = TRAITS_IMG
    traits_file = TRAITS_FILE
    traits_template = TRAITS_TEMPLATE
    if in_array(traits_img, trait):
        data = {
            'recipient': {'id': sender_id},
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': text,
                        'is_reusable': 'false'
                    }
                }
            }
        }
    elif in_array(traits_file, trait):
        data = {
            'recipient': {'id': sender_id},
            'message': {
                'attachment': {
                    'type': 'file',
                    'payload': {
                        'url': text,
                        'is_reusable': 'true'
                    }
                }
            }
        }
    elif in_array(traits_template, trait):
        if trait == 'templateWeb':
            data = {
                'recipient': {'id': sender_id},
                'message': {
                    'attachment': {
                        'type': 'template',
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'title': 'Welcome!',
                                    'image_url': 'https://4.bp.blogspot.com/-TNeiPeaE9a4/X_iEGiyzQJI/AAAAAAAAAMQ'
                                                 '/sWuRoW1nP7wKMybUcNaAikKrzOWULmlXgCK4BGAYYCw/s244/logo-v3.png',
                                    'subtitle': 'AtharizzBetta is Betta Breeder - Area 6',
                                    'default_action': {
                                        'type': 'web_url',
                                        'url': 'https://atharizzbetta.blogspot.com/p/about-us.html',
                                        'webview_height_ratio': 'tall',
                                    },
                                    'buttons': [
                                        {
                                            'type': 'web_url',
                                            'url': 'https://atharizzbetta.blogspot.com/',
                                            'title': 'View Website'
                                        },
                                        {
                                            'type': 'web_url',
                                            'title': 'WA Chatting',
                                            'url': 'https://api.whatsapp.com/send?phone=6285282793816'
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        else:
            attc = json.loads(text)
            data = {
                'recipient': {'id': sender_id},
                'message': attc
            }
    elif trait == 'get_json_content':
        response_only = True
        json_content = get_json_content(text, response_only)
        attc = json.loads(json_content)
        data = {
            'recipient': {'id': sender_id},
            'message': attc
        }
    else:
        trait = "text_message"
        data = {
            'recipient': {'id': sender_id},
            'message': {'text': text}
        }

    print(trait)
    print(str(data))
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/v2.8/me/messages?' + qs,
                         json=data)
    return resp.content


def url_encode(item_code):
    query = item_code.upper()
    return urllib.parse.quote(query)


def get_json_content(item_code, response_only):
    ts = url_encode(item_code)
    url = DASHBOARD_URL + url_encode(item_code)
    print(f'url: {url}')
    print(f'item_code: {ts}')
    response = requests.get(
        url,
        params={},
    )
    json_response = response.json()

    if response_only is None:
        if json_response:
            print(type(json_response))
            return json_response

    if json_response and json_response['attachment']:
        item = json_response
        json_string = json.dumps(item, indent=4)
        content = json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))

        if response_only is True:
            print(type(json_string))
            print(f'Output: {json_string}')
            return json_string
        else:
            print(type(content))
            print(f'Output-content: {str(content)}')
            return content

    return None


def first_trait_value(traits, trait):
    """
    Returns first trait value
    """
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


def handle_message(response, fb_id, msg):
    """
    Customizes our response to the message and sends it
    """
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_trait_value(response['traits'], 'wit$greetings')

    traits = TRAITS_LIST
    trait = None
    ts = None

    for x in traits:
        trait = first_trait_value(response['traits'], x)
        if trait:
            ts = x
            print(ts)
            break

    if greetings:
        text = "hello!"
    elif trait:
        text = trait
    else:
        response_only = None
        json_content = get_json_content(msg, response_only)
        if json_content:
            text = msg
            ts = "get_json_content"
        else:
            text = None

    # send message
    if text:
        fb_message(fb_id, text, ts)


# Python code to check for val in list
def in_array(traits, trait):
    if trait not in traits:
        return None
    return trait


def test_message(text):
    resp = client.message(text)
    print('Yay, got Wit.ai response: ' + str(resp))


# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

if __name__ == '__main__':
    # Run Server
    # app.run(host='0.0.0.0', port=argv[1])
    # app.run(host='127.0.0.1', port='8080')
    # test_message('berapa harganya?')

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
