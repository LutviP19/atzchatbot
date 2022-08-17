# Python code to check for val in list
import urllib.parse

import requests
import json
from types import SimpleNamespace

#DASHBOARD_URL = "http://localhost:3000/content/tpl/"
DASHBOARD_URL = "https://atz-dashboard.herokuapp.com/content/tpl/"


def in_array(traits, trait):
    if trait not in traits:
        return None
    return trait


traits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
test = in_array(traits=[], trait=None)
print(len(traits))

if test:
    print(test)

sender_id = '12345678'
text = r'''{
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'template',
            'elements': [{
                'media_type': 'image',
                'url':'https://web.facebook.com/photo.php?fbid=113532743640635&set=pb.100049517302876.-2207520000..&type=3',
                'buttons':[{
                    'type':'web_url',
                    'url':'https://www.tokopedia.com/proweb21/ikan-cupang-giant-multicolor',
                    'title':'BuyNow'
                }]
            }]
        }
    }
}'''


# print('The JSON String is', text)
# attc = json.loads(text)
# print(type(attc))
# print(str(attc))
#
# print(type(attc))
# data = {'recipient': {'id': sender_id}, "message": attc}
# print(type(data))
# print(str(data))
# for x in traits:
#     if x == 'banana':
#         print(traits.index())

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


itemCode = "ABCD"
response_only = True
json_content = get_json_content(itemCode, response_only)
if json_content and response_only is False:
    print(json_content)
    print(json_content.type)
    print(json_content.payload)
    print(json_content.payload.template_type)
    print(json_content.payload.elements[0].title)
elif json_content and response_only is True:
    if json_content:
        attc = json.loads(json_content)
        print(type(attc))
        print(attc)
else:
    if json_content:
        print(json_content)
