import requests, json, multiprocessing

facebook_token = 'CAAGm0PX4ZCpsBAGgRgA9kFSD7lK5bkU2G4hqYjrVcVa4o9SZCnpEPV8QFjFO1uFGj3JEYUoVoFrRmmUji3FZCogJEKgLJtgeR0hGDBs8rZBgmt1xrZBzWxm7ZBaM8KB54ZCtmg12zLxKU0ENmSPHgLpyCTMKTDd2LNZAe2JbACre9ksa3rXANufG2xZCkBmesY4AUtvf0Kpw7tp6cVf7SiXwtJVeFGBF0BuwZD' #get this from the api explorer or something
facebook_id = '100000178479403'

loginCredentials = {'facebook_token':facebook_token, 'facebook_id' : facebook_id}
headers = {'Content-Type' : 'application/json', 'User-Agent' : 'Tinder Android Version 3.2.0'}

r = requests.post('https://api.gotinder.com/auth', data=json.dumps(loginCredentials), headers=headers)
x_auth_token = r.json()['token']


def process_girl(girl):
    _id = girl['_id']
    name = girl['name']
    headers3 = {'X-Auth-Token' : x_auth_token, 'User-Agent' : 'Tinder Android Version 3.2.0'}
    r3 = requests.get('https://api.gotinder.com/like/' + _id, headers=headers3)
    print name, ":", girl['bio'].replace("\n", " ")


count = 0
while True:
    headers2 = {'User-Agent' : 'Tinder Android Version 3.2.0', 'Content-Type' : 'application/json', 'X-Auth-Token' : x_auth_token}
    r2 = requests.get('https://api.gotinder.com/user/recs', headers=headers2)
    girls = r2.json()['results']

    processes = []
    for girl in girls:
        process = multiprocessing.Process(target = process_girl, args = (girl,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    count += len(processes)

    print count, "Girls Liked"

