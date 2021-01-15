from redditClient import RedditClient
from financeClient import FinanceClient
from graphingClient import GraphingClient

def main():

    redditClient = RedditClient()
    redditClient.test()

    financeClient = FinanceClient()
    hist = financeClient.test()

    graphingClient = GraphingClient()
    graphingClient.test(hist)

if __name__ == "__main__":
    main()
