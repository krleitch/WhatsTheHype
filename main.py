import sys, getopt, json

from redditClient import RedditClient, RedditConfig
from financeClient import FinanceClient
from graphingClient import GraphingClient

class WhatsTheHype:

    def __init__(self, argv):

        # process args
        try:
            opts, args = getopt.getopt(argv,'hct:s:b:a:o:v',['help','config','ticker=','subreddit=','before=','after=','operation=','verbose'])
        except getopt.GetoptError:
            print('main.py -t <ticker> -s <subreddit> -b # -a #-c <redditConfigLocation> -o <links/comments/all> - v')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h',  '--help'):
                print('main.py -t <ticker> -s <subreddit> -b # -a # -c <redditConfigLocation> -o <links/comments/all> -v')
                sys.exit()
            elif opt in ('-c', '--config'):
                self.redditConfig = arg
            elif opt in ('-t', '--ticker'):
                self.ticker = arg.lower()
            elif opt in ('-s', '--subreddit'):
                self.subreddit = arg.lower()
            elif opt in ('-b', '--before'):
                self.before = int(arg)
            elif opt in ('-a', '--after'):
                self.after = int(arg)
            elif opt in ('-o', '--operation'):
                self.operation = arg.lower()
            elif opt in ('-v', '--verbose'):
                self.verbose = True

        # check period is valid
        try:
            assert(self.before > 0)
            assert(self.after > 0)
            assert(self.before < self.after)
        except AssertionError:
            # TODO: Make this give more info for which assert
            print('Invalid Before and/or After')

        # all tickers are less than 5
        try:
            assert(len(self.ticker) <= 5)   
        except AssertionError:
            print('Invalid Ticker')
         
        # check operation is valid, or set operation to default
        try:
            if ( not hasattr(self, 'operation') ):
                self.operation = 'all'
            else:
                assert(self.operation in ['links', 'comments', 'all'])
        except AssertionError:
            print('Operation must be of of links/comments/all')

        # Set verbose if not supplied
        if (not hasattr(self, 'verbose')):
            self.verbose = False
        
        # open reddit config
        defaultConfigLocation = 'redditConfig.json'
        with open(self.redditConfig if hasattr(self, 'redditConfig') else defaultConfigLocation) as f:
            rc: RedditConfig = json.load(f)

        # init clients
        self.redditClient = RedditClient(rc, self.verbose)
        self.financeClient = FinanceClient(self.ticker)
        self.graphingClient = GraphingClient(self.ticker, self.subreddit, self.operation)

    def main(self):

        # get data frames
        subredditDataForPeriod = self.redditClient.getSubredditDataForPeriod(self.subreddit, self.ticker, self.before, self.after, self.operation)
        tickerHistoryForPeriod = self.financeClient.getTickerHistoryForPeriod(self.before, self.after)

        # print statements
        if (self.verbose):
            print(subredditDataForPeriod)
            print(tickerHistoryForPeriod)

        # graph data frames
        self.graphingClient.graphTickerAndSubredditData(subredditDataForPeriod, tickerHistoryForPeriod, self.operation)

if __name__ == "__main__":

    # process args and run the program
    wth = WhatsTheHype(sys.argv[1:])
    wth.main()
