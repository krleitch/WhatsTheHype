import requests
import json

class RedditClient:

    def __init__(self, redditConfig: dict[str, str]) -> None:

        # setup basic auth
        auth = requests.auth.HTTPBasicAuth(redditConfig['clientId'], redditConfig['secret'])
        data = {'grant_type': 'password', 'username': redditConfig['username'], 'password': redditConfig['password']}
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # get auth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
        TOKEN = res.json()['access_token']

        # add auth token to headers
        self.headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    def getSubredditMentionsForPeriod(self, subreddit: str, ticker: str, period: str):

        # At the time of writing this the pushshift api has aggs parameter disabled
        # If it is ever enabled you can use aggs to get frequency data easier
        # eg.
        # https://api.pushshift.io/reddit/search/comment/?q=tsla&after=7d&aggs=created_utc&frequency=hour&size=0

        # payload = {'q': ticker, 'restrict_sr': 'on'}
        # url = 'https://oauth.reddit.com/r/' + subreddit + '/search.json'
        # test = requests.get(url, params=payload, headers=self.headers)
        # return len(test.json()['data']['children'])
        # gets titles
        # for i in (test.json()['data']['children']):
            # print(i['data']['title'])

        a= ''
        f = ''
        if (period == 'day' ):
            a = '1d'
            f = 'hour'
        elif (period == 'week'):
            a = '7d'
            f = 'day'
        elif (period == 'month'):
            a = '30d'
            f = 'day'
        elif (period == 'year'):
            a = '365d'
            f = 'day'
        else:
            a = 'all'
            f = 'day'

        payload = {'q': ticker, 'after': a, 'aggs': 'created_utc', 'frequency': f, 'size': 0, 'subreddit': subreddit}
        url = 'https://api.pushshift.io/reddit/search/comment/?q=trump&after=7d&aggs=created_utc&frequency=hour&size=0'
        mentions = requests.get(url)
        print(mentions.json())
        print(mentions.json()['data']['aggs']['created_utc'])
        return mentions.json()['data']['aggs']['created_utc']
