import requests, json, time
import pandas as pd
import numpy as np
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


    # before: #d
    # after: #d
    def __getSubredditDataForLinksForPeriod(self, subreddit: str, ticker: str, before: int, after: int, mentions):

        # t only supports day/week/month/year/all
        t = None
        if ( after <= 1 ):
            t = 'day'
        elif ( after <= 7 ):
            t = 'week'
        elif ( after <= 30 ):
            t = 'month'
        elif ( after <= 365 ):
            t = 'year'
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
    def __getSubredditDataForCommentsForPeriod(self, subreddit: str, ticker: str, before: int, after: int, mentions):

        str_after = str(after + 1) + 'd'
        str_before = str(before) + 'd'

        # make the request for comments of the subreddit mentioning the ticker
        payload = {'q': ticker, 'before': str_before, 'after': str_after, 'subreddit': subreddit, 'limit': 500, 'sort': 'desc'}
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

        # unique link_id per day
        unique = {}
        totalUsed = 0
        # fill in mentions from comments
        for c in comments:
            date = datetime.utcfromtimestamp(c['created_utc'])
            str_date = date.strftime("%Y-%m-%d")
            # only take dates we care about
            if str_date in mentions :
                totalUsed += 1
                # add to unique mentions
                if ( not str_date in unique ):
                    unique[str_date] = {}
                if ( not c['link_id'] in unique[str_date] ):
                    mentions[str_date][2] += 1
                    unique[str_date][c['link_id']] = True
                # find max score for the day
                mentions[str_date][3] = max(c['score'], mentions[str_date][3])
                # keep track of total number of comments for the day
                mentions[str_date][4] += 1

        if (self.verbose):
            print(str(totalUsed) + '/' + str(totalReceived) + ' total comments aggregated')

    # the comment api data is not always up to date for every day
    # take an educated guess at when comment data is incomplete
    def __removeIncompleteCommentData(self, df):

        # if we have less than threshold # of comments, we are guessing that
        # seeing a 0 means incomplete data, not that there are actually 0 comments
        # don't include the 0's in the mean calculation
        threshold = 5
        avg = df['Comments'].replace(0, np.nan).mean()

        if ( avg > threshold ):
            # replace wtih pd.nan
            cols = ['Comments', 'Comments Max']
            df[cols] = df[cols].replace(0, np.nan)
        
        return df

    # after: #d
    # before: #d
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
            mentions[str_d] = [0,0,0,0,0]

        #  fill in mentions with included operations
        if (operation in ['links', 'all']):
            self.__getSubredditDataForLinksForPeriod(subreddit, ticker, before, after, mentions)

        if (operation in ['comments', 'all']):
            self.__getSubredditDataForCommentsForPeriod(subreddit, ticker, before, after, mentions)

        # calculate averages
        for key in mentions:
            if ( not mentions[key][0] == 0 ):
                mentions[key] = [mentions[key][0], mentions[key][1] // mentions[key][0], mentions[key][2], mentions[key][3], mentions[key][4]]

        # create the data frame
        df = pd.DataFrame.from_dict(mentions, orient='index', columns=['Links', 'Links Avg Score', 'Comments', 'Comments Max', 'Total Comments'])
        # convert index from string to datetime
        df.index = pd.to_datetime(df.index)

        # if we have incomplete comment data replace 0 with pd.nan
        df = self.__removeIncompleteCommentData(df)

        # return the filled in dataframe
        return df
