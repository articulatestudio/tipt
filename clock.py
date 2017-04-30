from apscheduler.schedulers.blocking import  BlockingScheduler
import datetime
sched=BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)


def timed_job():
    import requests
    import json

    base_url = "https://api.api.ai/v1/entities?v=20150910"

    headers = {
        "Authorization": "Bearer 39a6518ee71d48de9a4854ad82f33567",
        "Content-Type": "application/json; charset=utf-8"
    }

    from hubstorage import HubstorageClient

    hc = HubstorageClient(auth='a2616c10ca5947108962ca09855b3445')

    project = hc.get_project('142753')

    jobs = project.jobq.list()

    jobs_keys = []

    for j in jobs:
        jobs_keys.append(j['key'])

    last_items = hc.get_job(jobs_keys[0]).items.iter_values()

    comments_data = []

    odds_data = []

    horses = []
    matches = []
    tracks = []

    def create_horse_entity(horses):
        body = {
            "id": "80f817e8-23fb-4e8e-ba62-eca1fcef7c3a",
            "name": "horse_name",
            "entries": [
            ]
        }

        for horse in horses:
            entry = {
                "value": horse,
                "synonyms": [
                ]
            }

            body['entries'].append(entry)

        return json.dumps(body)

    def create_match_entity(matches):
        body = {
            "id": "4c552f7b-6886-4313-a2ee-5a287db81be1",
            "name": "matches",
            "entries": [
            ]
        }

        for match in matches:
            entry = {
                "value": match,
                "synonyms": [
                ]
            }

            body['entries'].append(entry)

        return json.dumps(body)

    def create_track_entities(tracks):
        body = {
            "id": "72c689ba-96a8-4b57-a41a-5faea6811147",
            "name": "tracks",
            "entries": [
            ]
        }

        for track in tracks:
            entry = {
                "value": track,
                "synonyms": [
                ]
            }

            body['entries'].append(entry)

        return json.dumps(body)

    for item in last_items:
        if 'comments' in item:
            comments_data.append(item)
        elif 'odds' in item:
            odds_data.append(item)

    for item in odds_data:

        matches.append(item['match'])

        if item['tournament'] not in tracks:
            tracks.append(item['tournament'])

    for item in comments_data:
        current_horses = item['horses']
        horses += current_horses


    horse_entity = create_horse_entity(horses)
    track_entity = create_track_entities(tracks)
    match_entity = create_match_entity(matches)
    print "horse_entity", "track_entity", "match_entity"
    horses = requests.put(url=base_url, headers=headers, data=horse_entity)
    tracks = requests.put(url=base_url, headers=headers, data=track_entity)
    matches = requests.put(url=base_url, headers=headers, data=match_entity)



# sched.start()
timed_job
