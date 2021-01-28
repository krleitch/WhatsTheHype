import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self, ticker, subreddit):
        # plt configuration
        plt.close("all")
        # figure properties
        self.fig, self.axes = plt.subplots(nrows=1, ncols=3, sharex=True)
        self.fig.set_size_inches(22, 6)
        #  axes labels
        self.axes[0].set_ylabel('Price (USD)')
        self.axes[1].set_ylabel('Mentions')
        self.axes[2].set_ylabel('Avg Score')
        self.axes[0].set_xlabel('Date')
        self.axes[1].set_xlabel('Date')
        self.axes[2].set_xlabel('Date')
        # title
        plt.suptitle(ticker.upper() + ' Vs r/' + subreddit + ' Mentions Vs Average Score')

    def graphTickerAndSubredditData(self, subredditDataForPeriod, tickerHistoryForPeriod):

        # calculate the rolling average
        tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(50).mean()

        # we only have a single data point
        if (len(subredditDataForPeriod.index) == 1):
            # plot mentions
            subredditDataForPeriod['Mentions'].plot(ax=self.axes[1], style='bx')
            # plot prices
            tickerHistoryForPeriod[['Close', 'MA50']].plot(ax=self.axes[0], style='rx')
            # plot score
            subredditDataForPeriod['Avg Score'].plot(ax=self.axes[2], style='gx')
        else:
            # plot mentions
            subredditDataForPeriod['Mentions'].plot(ax=self.axes[1], style='b-')
            # plot prices
            tickerHistoryForPeriod[['Close', 'MA50']].plot(ax=self.axes[0], style='r-')
            # plot score
            subredditDataForPeriod['Avg Score'].plot(ax=self.axes[2], style='g-')   

        plt.legend()
        plt.show()

        # TODO: save graph
        #df.to_csv("foo.csv")
