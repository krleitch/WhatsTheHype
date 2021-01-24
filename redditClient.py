import requests, json
import pandas as pd
from datetime import datetime, timedelta

# TypedDict requires python 3.8+
# TODO: make compatible with python 3.7
from typing import TypedDict

class RedditConfig(TypedDict):
    username: str
    password: str
    clientId: str
    secret: str

class RedditClient:

    def __init__(self, redditConfig: RedditConfig) -> None:

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
        # example:
        # https://api.pushshift.io/reddit/search/comment/?q=tsla&after=7d&aggs=created_utc&frequency=hour&size=0

        # reddit api example
        # payload = {'q': ticker, 'restrict_sr': 'on'}
        # url = 'https://oauth.reddit.com/r/' + subreddit + '/search.json'
        # test = requests.get(url, params=payload, headers=self.headers)
        # return len(test.json()['data']['children'])
        # gets titles
        # for i in (test.json()['data']['children']):
            # print(i['data']['title'])

        a= ''
        if (period == 'day' ):
            a = '1d'
        elif (period == 'week'):
            a = '7d'
        elif (period == 'month'):
            a = '30d'
        elif (period == 'year'):
            a = '365d'
        else:
            a = 'all'

        # make the request for comments of the subreddit mentioning the ticker
        payload = {'q': ticker, 'after': a, 'subreddit': subreddit}
        url = 'https://api.pushshift.io/reddit/search/comment/'
        response = requests.get(url, params=payload)
        comments = response.json()['data']

        # create date range covering the period
        endDate = datetime.now()
        startDate = datetime.now() - timedelta(days=365)
        str_endDate = endDate.strftime("%Y/%m/%d")
        str_StartDate = startDate.strftime("%Y/%m/%d")
        dates = pd.date_range(start=str_StartDate, end=str_endDate, freq='D')

        # initialize mentions to 0
        mentions = {}
        for d in dates:
            str_d = d.strftime("%Y/%m/%d")
            mentions[str_d] = 0

        # fill in mentions from comments
        for c in comments:
            date = datetime.utcfromtimestamp(c['created_utc'])
            str_date = date.strftime("%Y/%m/%d")
            if str_date in mentions:
                mentions[str_date] += 1
            else:
                # fix error case
                print('error - unknown date')

        # create the data frame
        df = pd.DataFrame.from_dict(mentions, orient='index', columns=['mentions'])

        # return the filled in dataframe
        return df
