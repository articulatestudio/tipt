from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import apiai
from datetime import datetime, timezone, timedelta
from fractions import Fraction
from odds.mongo_handle import *
from odds.random_emoji import *

betting_companies = {"facebook": {"attachment": {"payload": {"elements": [
    {"subtitle": "Choose an option below", "title": "William Hill",
     "image_url": "https://williamhillplc.azureedge.net/cache/f/8/f/7/f/2/f8f7f24a88f4cd0246539fa2151143b6d8902366.png",
     "item_url": "http://sports.williamhill.com/bet/en-gb/betting/y/9/Horse+Racing.html", "buttons": [
        {"title": "Bet on Web", "type": "web_url",
         "url": "http://sports.williamhill.com/bet/en-gb/betting/y/9/Horse+Racing.html"},
        {"title": "Bet on App", "type": "web_url",
         "url": "http://sports.williamhill.com/bet/en-gb/betting/y/9/Horse+Racing.html"}]},
    {"subtitle": "Choose an option below", "title": "Paddy Power",
     "image_url": "https://pbs.twimg.com/profile_images/799595351984537600/V90FKR4J.jpg",
     "item_url": "http://www.paddypower.com/racing/",
     "buttons": [{"title": "Bet on Web", "type": "web_url", "url": "http://www.paddypower.com/racing/"},
                 {"title": "Bet on App", "type": "web_url", "url": "http://www.paddypower.com/racing/"}]},
    {"subtitle": "Choose an option below", "title": "Bet365",
     "image_url": "https://pbs.twimg.com/profile_images/423124117655531520/hXb2Vjwb_400x400.png",
     "item_url": "https://extra.bet365.com/promotions/horse-racing",
     "buttons": [{"title": "Bet on Web", "type": "web_url", "url": "https://extra.bet365.com/promotions/horse-racing"},
                 {"title": "Bet on App", "type": "web_url",
                  "url": "https://extra.bet365.com/promotions/horse-racing"}]},
    {"subtitle": "Choose an option below", "title": "Coral",
     "image_url": "http://www.slotssons.com/uk/wp-content/uploads/2016/02/coral-logo.png",
     "item_url": "http://sports.coral.co.uk/horse-racing",
     "buttons": [{"title": "Bet on Web", "type": "web_url", "url": "http://sports.coral.co.uk/horse-racing"},
                 {"title": "Bet on App", "type": "web_url", "url": "http://sports.coral.co.uk/horse-racing"}]},
    {"subtitle": "Choose an option below", "title": "Ladbrokes",
     "image_url": "http://www.betstudy.com/img/tags/ladbrokes.jpg",
     "item_url": "https://sports.ladbrokes.com/en-gb/racing/horse-racing/", "buttons": [
        {"title": "Bet on Web", "type": "web_url", "url": "https://sports.ladbrokes.com/en-gb/racing/horse-racing/"},
        {"title": "Bet on App", "type": "web_url", "url": "https://sports.ladbrokes.com/en-gb/racing/horse-racing/"}]},
    {"subtitle": "Choose an option below", "title": "BetVictor",
     "image_url": "http://betonstat.com/wp-content/uploads/betv3.jpg",
     "item_url": "www.betvictor.com/en/sports/horse-racing",
     "buttons": [{"title": "Bet on Web", "type": "web_url", "url": "www.betvictor.com/en/sports/horse-racing"},
                 {"title": "Bet on App", "type": "web_url", "url": "www.betvictor.com/en/sports/horse-racing"}]},
    {"subtitle": "Choose an option below", "title": "SkyBet",
     "image_url": "https://www.footy-tipster.co.uk/wp-content/uploads/2014/09/skybet.png",
     "item_url": "https://m.skybet.com/horse-racing",
     "buttons": [{"title": "Bet on Web", "type": "web_url", "url": "https://m.skybet.com/horse-racing"},
                 {"title": "Bet on App", "type": "web_url", "url": "https://m.skybet.com/horse-racing"}]},
    {"subtitle": "Choose an option below", "title": "Betway",
     "image_url": "http://cdn.howtoplay.org/wp-content/uploads/2016/03/betway_2.png",
     "item_url": "https://sports.betway.com/horse-racing/uk-and-ireland", "buttons": [
        {"title": "Bet on Web", "type": "web_url", "url": "https://sports.betway.com/horse-racing/uk-and-ireland"},
        {"title": "Bet on App", "type": "web_url", "url": "https://sports.betway.com/horse-racing/uk-and-ireland"}]}],
                                                             "template_type": "generic"}, "type": "template"}}}


collections = mongo.get_collections(DATABASE_NAME)
races_data, odds_data, tournaments_data, horses_data, predicts_data = mongo.get_data(collections=collections)


# def update_data():
#     global races_data
#     global odds_data
#     global tournaments_data
#     global horses_data
#     global predict_data
#     races_data, odds_data, tournaments_data, horses_data, predict_data = mongo.get_data(collections=collections)


def Home(request):
    return HttpResponse("The last update was")


@csrf_exempt
def replyhook(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        res = replyai(request_body)
        return JsonResponse(res)

    else:
        return HttpResponse("This method is not allowed: ")


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        print("Data: len()=tournaments_data" + str(len(tournaments_data)))
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        print("request body: " + str(body_unicode))
        res = action(request_body)
        print ("api-response: ")
        api_response = JsonResponse(res)
        print (api_response)
        api_response['Content-type'] = 'application/json'
        return api_response
    else:
        return HttpResponse('This method is not allowed!!!')


def get_current_time():
    """
    Get Current time
    """
    print((datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y%m%d%H%M"))
    iso_date = (datetime.now(timezone.utc) + timedelta(hours=-22)).isoformat()
    print('iso_date: {}'.format(iso_date))
    date = ((datetime.now(timezone.utc) + timedelta(hours=-22)).strftime("%Y%m%d%H%M"))
    year = date[:4]
    month_day = date[4:8]
    hour = date[8:10]
    minute = date[10:12]
    return {'iso_date': iso_date,
            'year': year,
            'm_day': month_day,
            'hour': hour,
            'minute': minute}


def replyai(data):
    query = data['query']

    ai = apiai.ApiAI('d96ab5f1e9bc4f22bffc3bafecb863df')

    request = ai.text_request()

    request.query = query

    response = request.getresponse().read()

    json_response = json.loads(response.decode('utf-8'))
    speech = json_response['result']['fulfillment']['speech']

    res = {"res": speech}

    return res


def getnextgame():

    data = odds_data[0]
    res = {}
    courses = []
    best_odds = None
    for item in tournaments_data:
        if item['name'] not in courses:
            courses.append(item['name'])

    res['tournament_id'] = data['tournament_id']
    res['tournament'] = data['tournament_name']

    for a in odds_data[0]['wagers']:
        best_odds = calc_best_odds(a)

    res['best_odds'] = best_odds

    speech = "The next game is " + str(data['name']) + ". "

    for item in res['best_odds']:
        cur_speech = "The best odds for " + str(item['name']) + " are "

        cur_speech = cur_speech + str(item['odd']) + r", "
        speech += cur_speech
    return speech


def calc_best_odds(odds=[]):
    """
    calculate best odds within 6
    """
    counter = 0
    best_odds = []

    if len(odds) == 0:
        return best_odds
    else:
        try:
            odds.sort(key=lambda x: float(x["odd"]), reverse=True)
            for item in odds:
                if counter > 6:
                    break
                best_odds.append(item)
                counter += 1
            print ('best_odds: {}'.format(best_odds))
        except Exception as e:
            print ('calc_best_odds: {}'.format(e))
            best_odds = []
    return best_odds


def convert_dec_frac(odd):
    """
    Retrieve the fraction value from Decimal value.
    """
    try:
        convert_odd = float(odd) - 1
        if convert_odd - int(convert_odd) == 0:
            result = "{}/1".format(str(int(convert_odd)))
            print('result: {}'.format(result))
            return result
        else:
            return str(Fraction(float(convert_odd)).limit_denominator())
    except Exception as e:
        print ('convert_dec_frac: {}'.format(e))
        return None


def on_courses(current_time):
    """
    return courses
    """
    courses = []
    for item in tournaments_data:
        if str(item['date']) <= str(current_time['iso_date']):
            continue
        elif item['name'] not in courses:
            courses.append(item['name'])
    return courses


def processHorseRequest(parameters):
    """
    Action is HorseOdds
    """

    horse = parameters['horse_name']
    vendors = []
    tournament = ""
    courses = []
    current_time = get_current_time()
    courses = on_courses(current_time=current_time)
    print('courses: {}'.format(courses))
    for a in odds_data:
        if horse in a['horse_name']:
            tournament = a['tournament_name']
            best_odds = calc_best_odds(a['wagers'])
            for item in best_odds:
                vendors.append(random_emoji(item['name']) + " " + item['name'] + " " + convert_dec_frac(item['odd']))

    if len(vendors) == 0:
        speech = "I'm struggling with that one. It could be that you made a typo, the race has already started or the horse isn't running today.:\n\n"

        quick_replies = []
        reply = text_quick_reply(title="Ask a human instead", payload="r_human")
        quick_replies.append(reply)



        final_data = apiai_facebook_quick_reply(text=speech, quick_replies=quick_replies)

        return final_data
    else:
        speech = ""

        speech = speech + "The best odds for " + horse_emoji + horse + " at " + tournament + " are:\n"

        for vendor in vendors:
            speech = speech + vendor + "\n"

        quick_replies = []
        reply = text_quick_reply(title="Bet Now", payload="Bet Now")
        quick_replies.append(reply)

        final_data = apiai_facebook_quick_reply(text=speech, quick_replies=quick_replies)

        return final_data


def processFootballRequest(parameters):
    match = parameters['TeamA'] + ' v ' + parameters['TeamB']
    teamA = parameters['TeamA']
    teamB = parameters['TeamB']
    bestTeamA = ""
    bestTeamB = ""
    bestDraw = ""
    bestVendorsA = ""
    bestVendorsB = ""
    bestVendorsD = ""

    for a in odds_data:
        if a['match'] == match:
            for key, value in a['odds'].items():
                if teamA in a['odds'] and teamB in a['odds'] and 'Draw' in a['odds']:
                    bestTeamA = a['odds'][teamA]['best']
                    bestTeamB = a['odds'][teamB]['best']
                    bestDraw = a['odds']['Draw']['best']

                    for k, v in a['odds'][teamA]['odds'].items():
                        if v == bestTeamA and key == teamA:
                            bestVendorsA = bestVendorsA + k + " with " + v + ","

                    for k, v in a['odds'][teamB]['odds'].items():
                        if v == bestTeamB and key == teamB:
                            bestVendorsB = bestVendorsB + k + " with " + v + ","

                    for k, v in a['odds']['Draw']['odds'].items():
                        if v == bestDraw and key == "Draw":
                            bestVendorsD = bestVendorsD + k + " with " + v + ","

    if bestTeamA == "" or bestTeamB == "" or bestDraw == "":
        speech = "We could not get the odds for those teams"

    else:
        speech = "The best odds for " + teamA + " winnning are " + bestTeamA + ". " + \
                 "The best vendors are: " + (bestVendorsA) + " " + \
                 "The best odds for " + teamB + " winning are " + bestTeamB + "." \
                                                                              "The best vendors are: " + (
                 bestVendorsB) + " " + \
                 "the best odds for a draw are " + bestDraw + ". " + \
                 "The best vendors are: " + (bestVendorsD) + " "

        speech = speech.replace(', ', '.', len(speech) - 2)

    return speech


def processData(data):
    if type(data) is dict:
        res = {
            "data": data,
            "source": "oddschecker-webhook"
        }

        return res
    elif type(data) is str:
        res = {
            "speech": data,
            "displayText": data,
            "source": "oddschecker-webhook"
        }

        return res


def showTimes(data):
    replies = []
    track = data['tracks']
    current_time = get_current_time()
    courses = on_courses(current_time=current_time)
    print('courses: {}'.format(courses))
    try:
        track_id = filter(lambda item: item['name'] == track and str(item['date']) <= current_time['iso_date'], tournaments_data)[0]['tournament_id']
        print ('track_id: {}'.format(track_id))
    except Exception as e:
        print ('Python 3 exception: {}'.format(e))
        try:
            track_id = next(filter(lambda item: item['name'] == track and str(item['date']) <= current_time['iso_date'], tournaments_data))['tournament_id']
        except Exception as e:
            print('Exception: {}'.format(e))
            track_id = ''

    print('trackid: {}'.format(track_id))

    if track_id == '':
        speech = "I see we've got racing from:\n\n"

        quick_replies = []

        for course in courses:
            reply = text_quick_reply(title=course, payload=course)
            quick_replies.append(reply)

        final_data = apiai_facebook_quick_reply(text=speech, quick_replies=quick_replies)

        return final_data
    else:
        for item in races_data:

            if item['tournament_id'] == track_id:
                match = track + " " + item['time']
                quick_reply = text_quick_reply(match, "get " + match)
                replies.append(quick_reply)

        if len(replies) > 0:
            final_data = apiai_facebook_quick_reply(
                "These are the next races at " + track + ". Select one of the races to get recommendations.",
                quick_replies=replies)

            return final_data

        else:
            speech = "I can see we have racing from:\n\n"

            quick_replies = []

            for course in courses:
                reply = text_quick_reply(title=course, payload=course)
                quick_replies.append(reply)

            final_data = apiai_facebook_quick_reply(text=speech, quick_replies=quick_replies)

            return final_data


def giveSuggestions(data):
    horse_emoji = u"\U0001F40E"
    match = data['matches']
    print("match is " + match)
    print("predict_data: {} ".format(predicts_data))

    predictions = ""
    speech = ""
    try:
        for item in predicts_data:
            print('race: {}'.format(item['Which racecourse?']))
            if item['Which racecourse?'] + ' ' + item['Race Time'] == match:
                try:
                    predictions = item["Horse Name"] + " is my pick in the " + item["Race Time"] + " at " + item['Which racecourse?'] + "\n\n"
                    predictions = predictions + item["Your recommendation text"]
                    print('recommendation: {}'.format(predictions))
                except Exception as e:
                    print('give suggestion error: {}'.format(e))
                    predictions = ""

        if predictions == "":
            speech = "It looks a tough field to split. My tip in this race is to keep your money in your pocket!"
        else:
            speech = speech + horse_emoji
            print('predictions: {}'.format(predictions))

            speech = speech + predictions + "\n"
        return speech

    except Exception as e:
        print ('giveSuggestions Error: {}'.format(e))
        speech = "I could not find predictions for that race"
        return speech


def default_fallback():
    courses = []
    for item in tournaments_data:
        if item['name'] not in courses:
            courses.append(item['name'])

    speech = "Oops! :( :( I  don't recognise that! Please select one of the courses to proceed.\n\n"

    quick_replies = []

    for course in courses:
        reply = text_quick_reply(title=course, payload=course)
        quick_replies.append(reply)

    final_data = apiai_facebook_quick_reply(text=speech, quick_replies=quick_replies)

    return final_data


def action(data):
    parameters = data['result']['parameters']
    print("action - parameters: " + str(parameters))
    if data['result']['metadata']['intentName'] == 'test':
        return processData(getnextgame())
    elif data['result']['action'] == 'HorseOdds':
        return processData(processHorseRequest(parameters))

    elif data['result']['action'] == 'next-race':
        return processData(showTimes(parameters))

    elif data['result']['action'] == 'next-race-postback':
        return processData(giveSuggestions(parameters))

    elif data['result']['action'] == 'bet_now':
        return processData(betting_companies)

    elif data['result']['action'] == 'input.unknown':
        return processData(default_fallback())

        # elif data['result']['metadata']['intentName'] == 'FootBallEPL':
        # return processRequest(processFootballRequest(parameters))


def text_quick_reply(title, payload):
    quick_reply = {
        "content_type": "text",
        "title": title,
        "payload": payload
    }
    return quick_reply


def apiai_facebook_quick_reply(text, quick_replies):
    reply = {"facebook": {
        "text": text,
        "quick_replies": quick_replies
    }
    }
    return reply
#
# if __name__ == '__main__':
#     showTimes({'tracks': 'Carlisle'})
