import requests
import json

class RedditClient:

    def __init__(self):

        # open config
        with open('redditConfig.json') as f:
            reddit = json.load(f)

        # setup basic auth
        auth = requests.auth.HTTPBasicAuth(reddit['clientId'], reddit['secret'])
        data = {'grant_type': 'password', 'username': reddit['username'], 'password': reddit['password']}
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # get auth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
        TOKEN = res.json()['access_token']

        # add auth token to headers
        self.headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    def test(self):

        payload = {'q': 'TSLA', 'restrict_sr': 'on'}
        test = requests.get('https://oauth.reddit.com/r/wallstreetbets/search.json', params=payload, headers=self.headers)

        # needed for comments
        # https://github.com/pushshift/api
        # test = requests.get('https://api.pushshift.io/reddit/search/comment/?q=science')
        # print(test.json()['data'][0].keys())

        # use
        # https://api.pushshift.io/reddit/search/comment/?q=tsla&after=24h&aggs=link_id&size=0

        # gets titles
        for i in (test.json()['data']['children']):
            print(i['data']['title'])
