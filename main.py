import requests
import json

def main():

    with open('reddit.json') as f:
        reddit = json.load(f)

    auth = requests.auth.HTTPBasicAuth(reddit['clientId'], reddit['secret'])
    data = {'grant_type': 'password', 'username': reddit['username'], 'password': reddit['password']}
    headers = {'User-Agent': 'MyBot/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    test = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    print(test.json())

if __name__ == "__main__":
    main()
