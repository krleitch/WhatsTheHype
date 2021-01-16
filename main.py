import sys, getopt

from redditClient import RedditClient
from financeClient import FinanceClient
from graphingClient import GraphingClient

class WhatsTheHype:

    def __init__(self, argv):

        # process args

        try:
            opts, args = getopt.getopt(argv,'ht:s:p:',['ticker=','subreddit','period='])
        except getopt.GetoptError:
            print('main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('main.py -t <ticker> -s <subreddit> -p <day/week/month/year/all>')
                sys.exit()
            elif opt in ("-t", "--ticker"):
                self.ticker = arg
            elif opt in ("-s", "--subreddit"):
                self.subreddit = arg
            elif opt in ("-p", "--period"):
                self.period = arg

        # init clients

        self.redditClient = RedditClient()
        self.financeClient = FinanceClient()
        self.graphingClient = GraphingClient()

    def main(self):

        subredditTickerCount = self.redditClient.getSubredditTickerCount(self.subreddit, self.ticker)
        tickerHistory = self.financeClient.getTickerHistory(self.ticker)        
        self.graphingClient.graphTickerAndHistory(subredditTickerCount, tickerHistory)

if __name__ == "__main__":
    wth = WhatsTheHype(sys.argv[1:])
    wth.main()
