import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class GraphingClient:

    def __init__(self, ticker, subreddit, operation):
        # plt configuration
        plt.close("all")
        # figure properties
        self.fig, self.axes = plt.subplots(nrows=1, ncols=3, sharex=True)
        self.fig.set_size_inches(24, 6)
        #  axes labels
        self.axes[0].set_ylabel('Price (USD)')
        self.axes[1].set_ylabel('Mentions')
        self.axes[2].set_ylabel('Average Score')
        self.axes[0].set_xlabel('Date')
        self.axes[1].set_xlabel('Date')
        self.axes[2].set_xlabel('Date')
        # create title
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        op_string = 'comments and links' if operation == 'all' else operation
        title = f'{ticker.upper()} on r/{subreddit} ({op_string}). Current Time: {dt_string}'
        plt.suptitle(title)
        # subplot titles
        self.axes[0].title.set_text(f'{ticker.upper()} Close Price')
        self.axes[1].title.set_text(f'r/{subreddit} Mentions')
        self.axes[2].title.set_text(f'Average Score of Mentions')

    def graphTickerAndSubredditData(self, subredditDataForPeriod, tickerHistoryForPeriod):

        # we only have a single data point
        if (len(subredditDataForPeriod.index) == 1):
            # plot mentions
            subredditDataForPeriod['Mentions'].plot(ax=self.axes[1], style='bx', label='Mentions')
            # plot prices
            tickerHistoryForPeriod['Close'].plot(ax=self.axes[0], style='rx', label='Close')
            # plot score
            subredditDataForPeriod['Avg Score'].plot(ax=self.axes[2], style='gx', label='Average Score')
        else:
            # plot mentions
            subredditDataForPeriod['Mentions'].plot(ax=self.axes[1], style='b-', label='Mentions')
            # plot prices
            tickerHistoryForPeriod['Close'].plot(ax=self.axes[0], style='r-', label='Close')
            # calculate the rolling average if data set is large enough
            if ( len(subredditDataForPeriod.index) >= 100  ):
                tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(50).mean()
                tickerHistoryForPeriod['MA50'].plot(ax=self.axes[0], style='y-', label='MA50')
            # plot score
            subredditDataForPeriod['Avg Score'].plot(ax=self.axes[2], style='g-', label='Average Score')   

        # grid
        self.axes[0].grid()
        self.axes[1].grid()
        self.axes[2].grid()
        # legend
        self.axes[0].legend()
        self.axes[1].legend()
        self.axes[2].legend()
        # show plots
        plt.show()

        # TODO: allow option to save graph
        #df.to_csv("foo.csv")
