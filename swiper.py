import requests, json, multiprocessing

config = open('config.txt', 'r').read().split('\n')
FB_ID = config[0]
FB_TOKEN = config[1]
LOGIN_CRED = {'facebook_token' : FB_TOKEN, 'facebook_id' : FB_ID}
MIN_FRIEND_COUNT = 15
URL = 'https://api.gotinder.com'

# Like a single girl and print out her name
def process_girl(girl, auth_token):
    tinder_id = girl['_id']
    name = girl['name']
    bio = girl['bio'].replace("\n", " ") # Remove new lines
    friend_count = girl['common_friend_count']
    headers = {'X-Auth-Token' : auth_token, 'User-Agent' : 'Tinder Android Version 3.2.0'}
    request = requests.get(URL + '/like/' + tinder_id, headers = headers)

    if friend_count > MIN_FRIEND_COUNT:
        # Friends
        print
        print 'Common Friend', name, '(' + str(friend_count) + '):', bio
        print
    elif 'snap' in bio.lower():
        # Snapchat
        print name, ':', bio
    else:
        print name


def main():
    # Authenticate
    headers = {'Content-Type' : 'application/json', 'User-Agent' : 'Tinder Android Version 3.2.0'}
    request = requests.post(URL + '/auth', data = json.dumps(LOGIN_CRED), headers = headers).json()

    if 'token' not in request:
        print 'Please Refresh FB Token'
        return

    auth_token = request['token']

    # Grab first 10
    liked = set()
    headers = {'User-Agent' : 'Tinder Android Version 3.2.0', 'Content-Type' : 'application/json', 'X-Auth-Token' : auth_token}
    request = requests.get(URL + '/user/recs', headers = headers).json()

    # Continue while there are more
    while 'results' in request:
        girls = request['results']
        processes = []

        for girl in girls:
            liked.add(girl['_id'])
            process = multiprocessing.Process(target = process_girl, args = (girl, auth_token))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        # Grab next 10
        request = requests.get(URL + '/user/recs', headers = headers).json()

    print len(liked), "Girls Liked"

if __name__ == "__main__":
    main()
