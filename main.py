import sys, getopt, json

from redditClient import RedditClient
from financeClient import FinanceClient
from graphingClient import GraphingClient

class WhatsTheHype:

    def __init__(self, argv):

        # process args
        try:
            opts, args = getopt.getopt(argv,'hct:s:p:',['config','ticker=','subreddit=','period='])
        except getopt.GetoptError:
            print('main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all> -c <redditConfigLocation>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all> -c <redditConfigLocation>')
                sys.exit()
            elif opt in ("-c", "--config"):
                self.redditConfig = arg
            elif opt in ("-t", "--ticker"):
                self.ticker = arg.lower()
            elif opt in ("-s", "--subreddit"):
                self.subreddit = arg.lower()
            elif opt in ("-p", "--period"):
                self.period = arg.lower()

        # check period one of day/week/month/year/all
        assert(self.period in ['day', 'week', 'month', 'year', 'all'])

        # all tickers are less than 5
        assert(len(self.ticker) <= 5)    

        # open config
        with open(self.redditConfig if self.redditConfig else 'redditConfig.json') as f:
            rc = json.load(f)

        # init clients
        self.redditClient = RedditClient(rc)
        self.financeClient = FinanceClient(self.ticker)
        self.graphingClient = GraphingClient()

    def main(self):
        subredditMentionsForPeriod = self.redditClient.getSubredditMentionsForPeriod(self.subreddit, self.ticker, self.period)
        tickerHistoryForPeriod = self.financeClient.getTickerHistoryForPeriod(self.period)
        self.graphingClient.graphTickerAndHistory(subredditMentionsForPeriod, tickerHistoryForPeriod)

if __name__ == "__main__":
    wth = WhatsTheHype(sys.argv[1:])
    wth.main()
