import requests, json, time
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

    # period: day/week/month/year/all
    def __getSubredditDataForPostsForPeriod(self, subreddit: str, ticker: str, period: str, mentions):

        # reddit api links search
        payload = {'q': ticker, 'restrict_sr': 'on', 't': period, 'limit': 100 }
        url = 'https://oauth.reddit.com/r/' + subreddit + '/search.json'
        response = requests.get(url, params=payload, headers=self.headers)
        after = response.json()['data']['after']
        links = response.json()['data']['children']
        
        # build links by using after
        while after:
            response = requests.get(url, params=payload, headers=self.headers)
            while response.status_code == 429:
                # TODO: use retry-after
                time.sleep(1)
                response = requests.get(url, params=payload, headers=self.headers )
            links += response.json()['data']['children']
            after =  response.json()['data']['after']
            payload['after'] = after

        # add links to mentions
        for l in links:
            date = datetime.utcfromtimestamp(l['data']['created'])
            str_date = date.strftime("%Y-%m-%d")
            if str_date in mentions:
                mentions[str_date][0] += 1
                mentions[str_date][1] += l['data']['score']
            else:
                # TODO: fix error case
                print('error - unknown link date')

    # after: #d or epoch time
    def __getSubredditDataForCommentsForPeriod(self, subreddit: str, ticker: str, after: str, mentions):

        # make the request for comments of the subreddit mentioning the ticker
        payload = {'q': ticker, 'after': after, 'subreddit': subreddit, 'limit': 500, 'sort': 'desc'}
        headers = {'User-Agent': 'MyBot/0.0.1'}
        url = 'https://api.pushshift.io/reddit/search/comment/'
        response = requests.get(url, params=payload, headers=headers )
        comments = response.json()['data']

        while len(response.json()['data']) > 0:
            # TODO: add progress statements
            before =  response.json()['data'][-1]['created_utc']
            payload['before'] = before
            response = requests.get(url, params=payload, headers=headers )
            while response.status_code == 429:
                # TODO: use retry-after
                time.sleep(1)
                response = requests.get(url, params=payload, headers=headers )
            comments += response.json()['data']

        # fill in mentions from comments
        for c in comments:
            date = datetime.utcfromtimestamp(c['created_utc'])
            str_date = date.strftime("%Y-%m-%d")
            if str_date in mentions:
                mentions[str_date][0] += 1
                mentions[str_date][1] += c['score']
            else:
                # TODO: fix error case
                print('error - unknown comment date')

    # period: day/week/month/year/all
    # operation: posts/comments/all
    def getSubredditDataForPeriod(self, subreddit: str, ticker: str, period: str, operation: str):

        # At the time of writing this the pushshift api has aggs parameter disabled
        # If it is ever enabled you can use aggs to get frequency data easier
        # example:
        # https://api.pushshift.io/reddit/search/comment/?q=tsla&after=7d&aggs=created_utc&frequency=hour&size=0

        after = ''
        # d is days backwards, so 0 for 1 day because we dont need any days before
        days = None
        if (period == 'day' ):
            after = '1d'
            days = 0
        elif (period == 'week'):
            after = '7d'
            days = 6
        elif (period == 'month'):
            after = '30d'
            days = 29
        elif (period == 'year'):
            after = '365d'
            days = 364
        else:
            after = 'all'
            days = 364

        # create date range covering the period
        endDate = datetime.now()
        startDate = datetime.now() - timedelta(days=days)
        str_endDate = endDate.strftime("%Y-%m-%d")
        str_StartDate = startDate.strftime("%Y-%m-%d")
        dates = pd.date_range(start=str_StartDate, end=str_endDate, freq='D')

        # initialize mentions to 0
        mentions = {}
        for d in dates:
            str_d = d.strftime("%Y-%m-%d")
            mentions[str_d] = [0,0]

        #  fill in mentions with included operations
        if (operation in ['posts', 'all']):
            self.__getSubredditDataForPostsForPeriod(subreddit, ticker, period, mentions)

        if (operation in ['comments', 'all']):
            self.__getSubredditDataForCommentsForPeriod(subreddit, ticker, after, mentions)

        # calculate average score
        for key in mentions:
            mentions[key] = [mentions[key][0], mentions[key][1] // mentions[key][0]]

        # create the data frame
        df = pd.DataFrame.from_dict(mentions, orient='index', columns=['Mentions', 'Avg Score'])
        # convert index from string to datetime
        df.index = pd.to_datetime(df.index)
        print(df)

        # return the filled in dataframe
        return df
