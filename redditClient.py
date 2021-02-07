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

    def __init__(self, redditConfig: RedditConfig, verbose: bool) -> None:

        # setup basic auth
        auth = requests.auth.HTTPBasicAuth(redditConfig['clientId'], redditConfig['secret'])
        data = {'grant_type': 'password', 'username': redditConfig['username'], 'password': redditConfig['password']}
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # get auth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
        TOKEN = res.json()['access_token']

        # add auth token to headers
        self.headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
        self.verbose = verbose

    # before: #
    # after: #
    def __getSubredditDataForLinksForPeriod(self, subreddit: str, ticker: str, before: int, after: int, mentions):

        t = None
        period = after-before
        if ( period <= 1 ):
            t = 'day'
        elif ( period <= 7 ):
            t = 'week'
        elif ( period <= 30 ):
            t = 'month'
        elif ( period <= 365 ):
            t = 'week'
        else:
            t = 'all'

        # reddit api links search
        payload = {'q': ticker, 'restrict_sr': 'on', 't': t, 'limit': 100 }
        url = 'https://oauth.reddit.com/r/' + subreddit + '/search.json'
        response = requests.get(url, params=payload, headers=self.headers)
        after = response.json()['data']['after']
        links = response.json()['data']['children']
        totalReceived = len(links)
        if (self.verbose):
            print(str(totalReceived) + ' Links Fetched', end="\r", flush=True)
        
        # build links by using after
        while after:
            response = requests.get(url, params=payload, headers=self.headers)
            while response.status_code == 429:
                # TODO: there is no retry-after header right now
                # time.sleep(int(response.headers["Retry-After"]))
                time.sleep(1)
                response = requests.get(url, params=payload, headers=self.headers )
            links += response.json()['data']['children']
            totalReceived = len(links)
            if (self.verbose):
                print(str(totalReceived) + ' Links Fetched', end="\r", flush=True)
            after =  response.json()['data']['after']
            payload['after'] = after
        
        totalUsed = 0
        # add links to mentions
        for l in links:
            date = datetime.utcfromtimestamp(l['data']['created'])
            str_date = date.strftime("%Y-%m-%d")
            #  only take dates we care about
            #  TODO: we still get the current day and this filters it out
            #        should change so that never get invalid dates here
            if str_date in mentions:
                totalUsed += 1
                mentions[str_date][0] += 1
                mentions[str_date][1] += l['data']['score']

        if (self.verbose):
            print(str(totalUsed) + '/' + str(totalReceived) + ' total links aggregated')

    # after: #d or epoch time
    def __getSubredditDataForCommentsForPeriod(self, subreddit: str, ticker: str, after: int, mentions):

        str_after = str(after) + 'd'

        # make the request for comments of the subreddit mentioning the ticker
        payload = {'q': ticker, 'after': str_after, 'subreddit': subreddit, 'limit': 500, 'sort': 'desc'}
        headers = {'User-Agent': 'MyBot/0.0.1'}
        url = 'https://api.pushshift.io/reddit/search/comment/'
        response = requests.get(url, params=payload, headers=headers )
        comments = response.json()['data']
        totalReceived = len(comments)
        if (self.verbose):
            print(str(totalReceived) + ' Comments Fetched', end="\r", flush=True)

        while len(response.json()['data']) > 0:
            before =  response.json()['data'][-1]['created_utc']
            payload['before'] = before
            response = requests.get(url, params=payload, headers=headers )
            while response.status_code == 429:
                # TODO: there is no retry-after header right now
                # time.sleep(int(response.headers["Retry-After"]))
                time.sleep(1)
                response = requests.get(url, params=payload, headers=headers )
            comments += response.json()['data']
            totalReceived = len(comments)
            if (self.verbose):
                print(str(totalReceived) + ' Comments Fetched', end="\r", flush=True)

        totalUsed = 0
        # fill in mentions from comments
        for c in comments:
            date = datetime.utcfromtimestamp(c['created_utc'])
            str_date = date.strftime("%Y-%m-%d")
            # only take dates we care about
            if str_date in mentions:
                totalUsed += 1
                mentions[str_date][0] += 1
                mentions[str_date][1] += c['score']

        if (self.verbose):
            print(str(totalUsed) + '/' + str(totalReceived) + ' total comments aggregated')

    # after: #
    # operation: links/comments/all
    def getSubredditDataForPeriod(self, subreddit: str, ticker: str, before: int, after: int, operation: str):

        # At the time of writing this the pushshift api has aggs parameter disabled
        # If it is ever enabled you can use aggs to get frequency data easier
        # example:
        # https://api.pushshift.io/reddit/search/comment/?q=tsla&after=7d&aggs=created_utc&frequency=hour&size=0

        # create date range covering the period ( after-before )
        # starts from 1 day ago, since we dont get data for current day all the time
        endDate = datetime.now() - timedelta(days=before)
        startDate = datetime.now() - timedelta(days=after)
        str_endDate = endDate.strftime("%Y-%m-%d")
        str_StartDate = startDate.strftime("%Y-%m-%d")
        dates = pd.date_range(start=str_StartDate, end=str_endDate, freq='D')

        # initialize mentions to 0
        mentions = {}
        for d in dates:
            str_d = d.strftime("%Y-%m-%d")
            mentions[str_d] = [0,0]

        #  fill in mentions with included operations
        if (operation in ['links', 'all']):
            self.__getSubredditDataForLinksForPeriod(subreddit, ticker, before, after, mentions)

        if (operation in ['comments', 'all']):
            self.__getSubredditDataForCommentsForPeriod(subreddit, ticker, after, mentions)

        # calculate average score
        for key in mentions:
            if ( not mentions[key][0] == 0 ):
                mentions[key] = [mentions[key][0], mentions[key][1] // mentions[key][0]]

        # create the data frame
        df = pd.DataFrame.from_dict(mentions, orient='index', columns=['Mentions', 'Avg Score'])
        # convert index from string to datetime
        df.index = pd.to_datetime(df.index)

        # return the filled in dataframe
        return df
