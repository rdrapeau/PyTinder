import requests, json

config = open('config.txt', 'r').read().split('\n')
FB_ID = config[0]
FB_TOKEN = config[1]
LOGIN_CRED = {'facebook_token' : FB_TOKEN, 'facebook_id' : FB_ID}
MIN_FRIEND_COUNT = 15
URL = "https://api.gotinder.com/"
LAST_ACTIVITY = '2014-05-25T21:55:14.181Z'
LIMIT = 25


def main():
    # Authenticate
    headers = {'Content-Type' : 'application/json', 'User-Agent' : 'Tinder Android Version 3.2.0'}
    request = requests.post(URL + '/auth', data = json.dumps(LOGIN_CRED), headers = headers).json()

    if 'token' not in request:
        print 'Please Refresh FB Token'
        return

    # Get matches since last activity date
    auth_token = request['token']
    headers = {'User-Agent' : 'Tinder Android Version 3.2.0', 'Content-Type' : 'application/json', 'X-Auth-Token' : auth_token}
    data = json.dumps({'last_activity_date': LAST_ACTIVITY})
    request = requests.post(URL + '/updates', headers = headers, data = data).json()

    matches = list(request['matches'])
    matches.sort(key = lambda match : match['last_activity_date'], reverse = True)

    for match in matches[:LIMIT]:
        if 'person' in match:
            print match['person']['name'], ':', match['person']['bio'].replace("\n", "")
            print


if __name__ == "__main__":
    main()
