import json
import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import apiai


def get_connect_headers():
    base_url = 'https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token'
    client_id = 'e46b50be-afdf-4104-bd14-dd6c3c8d745f'
    client_secret = 'EgvPtohyBQ6LpjddcuihO0F'

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://api.botframework.com/.default'
    }

    res = requests.post(base_url, data=data)

    access_token = res.json()['access_token']

    connect_headers = {
        'Authorization': "Bearer " + str(access_token),
        'Content-Type': 'application/json; charset=utf-8'
    }

    return connect_headers


def get_needed_data(res):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")
    from_data = res['recipient']
    conversation_data = res['conversation']
    recipient_data = res['from']
    reply_to_id = res['from']['id']

    service_url = res['serviceUrl']

    responseURL = service_url + "v3/conversations/%s/activities/%s" % (conversation_data["id"], reply_to_id)

    data = {}
    data['timestamp'] = timestamp
    data['from_data'] = from_data
    data['conversation_data'] = conversation_data
    data['recipient_data'] = recipient_data
    data['reply_id'] = reply_to_id
    data['service_url'] = service_url
    data['responseURL'] = responseURL

    return data


@csrf_exempt
def skype_webhook(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)

        print(request_body)

        handle_apiai(request_body)

        return HttpResponse('')

    else:
        return HttpResponse('This method is not allowed!!!')


def send_message(data, message):
    connect_headers = get_connect_headers()

    payload = {
        "type": "message",
        "timestamp": data['timestamp'],
        "from": data['from_data'],
        "conversation": data['conversation_data'],
        "recipient": data['recipient_data'],
        "replyToId": data['reply_id'],
        "text": message
    }

    responseURL = data['responseURL']
    res = requests.post(responseURL, data=json.dumps(payload), headers=connect_headers)
    print(res.text)


def send_attachement(data, message, attachments):
    connect_headers = get_connect_headers()

    payload = {
        "type": "message",
        "timestamp": data['timestamp'],
        "from": data['from_data'],
        "conversation": data['conversation_data'],
        "recipient": data['recipient_data'],
        "replyToId": data['reply_id'],
        "text": message,
        "attachments": attachments
    }

    responseURL = data['responseURL']
    res = requests.post(responseURL, data=json.dumps(payload), headers=connect_headers)
    print(res.text)


def handle_apiai(resa):
    query = resa['text']

    ai = apiai.ApiAI('20e077680641429b895638ba65065676')

    request = ai.text_request()

    request.query = query

    response = request.getresponse().read()

    json_response = json.loads(response.decode('utf-8'))

    print(json_response)
    speech = json_response['result']['fulfillment']['speech']
    action = json_response['result']['action']

    if action == "mandatory":
        image = create_main_image(url='http://i.share.pho.to/9e286c5c_o.png', name="partnerFunction")
        attachments = []
        attachments.append(image)
        send_attachement(get_needed_data(resa), message=speech, attachments=attachments)

    elif action == "invalid_post":
        image = create_main_image(
            url='http://i.share.pho.to/4a7dcad4_o.png',
            name="invalidPost")

        images = []
        images.append(image)
        send_attachement(get_needed_data(resa), message=speech, attachments=images)

        return

    elif action == 'launch':
        buttons = []
        button1 = create_button('postBack', "Ok", 'vendor request okay')
        button2 = create_button('postBack', "Not Ok", "vendor request not okay")
        buttons.append(button1)
        buttons.append(button2)
        images = []
        hero_card = create_hero_card(title='', subtitle='logged on?', buttons=buttons, images=images)

        attachments = []
        attachments.append(hero_card)
        send_attachement(data=get_needed_data(resa), message=speech, attachments=attachments)

        return

    elif action == 'vendorrequestokay':

        images = []
        image = create_main_image(url='http://i.share.pho.to/ca54c695_o.png', name="searchVendor")
        images.append(image)
        send_attachement(get_needed_data(resa), message="", attachments=images)

        buttons = []
        button1 = create_button('postBack', "Yes", 'user got it')
        button2 = create_button('postBack', "NO", "user did not get it")
        buttons.append(button1)
        buttons.append(button2)
        images = []
        hero_card = create_hero_card(title='', subtitle='Got it?', buttons=buttons, images=images)

        attachments = []
        attachments.append(hero_card)
        send_attachement(data=get_needed_data(resa), message=speech, attachments=attachments)

        return

    elif action == 'usergotit':

        images = []
        image = create_main_image(
            url='http://i.share.pho.to/18eb82a2_o.png',
            name="changeRecords")
        images.append(image)
        send_attachement(get_needed_data(resa), message="", attachments=images)

        buttons = []
        button1 = create_button('postBack', "Yes", 'yes move')
        button2 = create_button('postBack', "NO", "no do not move")
        buttons.append(button1)
        buttons.append(button2)
        images = []
        hero_card = create_hero_card(title='', subtitle='You ok to move from here?', buttons=buttons, images=images)

        attachments = []
        attachments.append(hero_card)
        send_attachement(data=get_needed_data(resa), message=speech, attachments=attachments)

        return

    elif action == "classified":
        image = create_main_image(
            url='http://i.share.pho.to/716f5555_o.png',
            name="supplyType")
        attachments = []
        attachments.append(image)
        send_attachement(get_needed_data(resa), message=speech, attachments=attachments)

        return

    elif action == "purchasing":
        image = create_main_image(
            url='http://i.share.pho.to/3f4dba78_o.png',
            name="vendorPurchase")
        attachments = []
        attachments.append(image)
        send_attachement(get_needed_data(resa), message=speech, attachments=attachments)

        return

    else:
        send_message(get_needed_data(resa), speech)
        return


def create_hero_card(title, subtitle, images, buttons):
    hero_card = {
        "contentType": "application/vnd.microsoft.card.hero",
        "content": {
            "title": title,
            "subtitle": subtitle,
            "images": images,
            "buttons": buttons
        }
    }

    return hero_card


def create_button(type, title, value):
    image = {
        "type": type,
        "title": title,
        "value": value
    }

    return image


def create_image(url):
    image = {
        "url": url
    }

    return image


def create_main_image(url, name):
    image = {
        "contentType": "image/png",
        "contentUrl": url,
        "name": name
    }
    return image
