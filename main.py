import sys, getopt, json

from redditClient import RedditClient, RedditConfig
from financeClient import FinanceClient
from graphingClient import GraphingClient

class WhatsTheHype:

    def __init__(self, argv):

        # process args
        redditConfig: str = None
        try:
            opts, args = getopt.getopt(argv,'hct:s:p:o:v',['help','config','ticker=','subreddit=','period=','operation=','verbose'])
        except getopt.GetoptError:
            print('main.py -t <ticker> -s <subreddit> -p <day/week/month/quarter/half/year/all> -c <redditConfigLocation> -o <posts/comments/all> - v')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h',  '--help'):
                print('main.py -t <ticker> -s <subreddit> -p <day/week/month/quarter/half/year/all> -c <redditConfigLocation> -o <posts/comments/all> -v')
                sys.exit()
            elif opt in ('-c', '--config'):
                redditConfig = arg
            elif opt in ('-t', '--ticker'):
                self.ticker = arg.lower()
            elif opt in ('-s', '--subreddit'):
                self.subreddit = arg.lower()
            elif opt in ('-p', '--period'):
                self.period = arg.lower()
            elif opt in ('-o', '--operation'):
                self.operation = arg.lower()
            elif opt in ('-v', '--verbose'):
                self.verbose = True

        # check period one of day/week/month/year/all
        assert(self.period in ['day', 'week', 'month', 'year', 'all'])

        # all tickers are less than 5
        assert(len(self.ticker) <= 5)    

        # check operation is valid, or set operation to default
        try:
            assert(self.operation in ['posts', 'comments', 'all'])
        except AssertionError:
            self.operation = 'all'

        # Set verbose
        if (not hasattr(self, 'verbose')):
            self.verbose = False
        
        # open reddit config
        with open(redditConfig if redditConfig else 'redditConfig.json') as f:
            rc: RedditConfig = json.load(f)

        # init clients
        self.redditClient = RedditClient(rc)
        self.financeClient = FinanceClient(self.ticker)
        self.graphingClient = GraphingClient(self.ticker, self.subreddit)

    def main(self):
        subredditDataForPeriod = self.redditClient.getSubredditDataForPeriod(self.subreddit, self.ticker, self.period, self.operation)
        tickerHistoryForPeriod = self.financeClient.getTickerHistoryForPeriod(self.period)

        # print statements
        if (self.verbose):
            print(subredditDataForPeriod)
            print(tickerHistoryForPeriod)

        self.graphingClient.graphTickerAndSubredditData(subredditDataForPeriod, tickerHistoryForPeriod)

if __name__ == "__main__":
    wth = WhatsTheHype(sys.argv[1:])
    wth.main()
