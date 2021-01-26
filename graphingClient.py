import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self, ticker, subreddit):
        # plt configuration
        plt.close("all")
        self.fig, self.axes = plt.subplots(nrows=1, ncols=3, sharex=True)
        self.fig.set_size_inches(20, 6)
        self.axes[0].set_ylabel('Price (USD) ')
        self.axes[1].set_ylabel('Mentions')
        self.axes[2].set_ylabel('Score')
        plt.suptitle(ticker.upper() + ' Vs r/' + subreddit + ' Mentions VS Score')

    def graphTickerAndHistory(self, subredditMentionsForPeriod, tickerHistoryForPeriod):

        # calculate the rolling average
        tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(50).mean()

        # we only have a single data point
        if (len(tickerHistoryForPeriod.index) == 1 ):
            # plot prices
            tickerHistoryForPeriod[['Close', 'MA50']].plot(ax=self.axes[0], style='rx')
            # plot mentions
            subredditMentionsForPeriod['Mentions'].plot(ax=self.axes[1], style='bx')
            # plot score
            subredditMentionsForPeriod['Score'].plot(ax=self.axes[2],  style='gx')
        else:
            # plot prices
            tickerHistoryForPeriod[['Close', 'MA50']].plot(ax=self.axes[0], style='r-')
            # plot mentions
            subredditMentionsForPeriod['Mentions'].plot(ax=self.axes[1], style='b-')
            # plot score
            subredditMentionsForPeriod['Score'].plot(ax=self.axes[2], style='g-')   

        plt.legend()
        plt.show()

        # TODO: save graph
        #df.to_csv("foo.csv")
