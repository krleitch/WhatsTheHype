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
        self.fig.set_size_inches(24, 8)
        #  axes labels
        self.axes[0].set_ylabel('Price (USD)')
        self.axes[1].set_ylabel('Mentions')
        self.axes[2].set_ylabel('Upvotes')
        self.axes[0].set_xlabel('Date')
        self.axes[1].set_xlabel('Date')
        self.axes[2].set_xlabel('Date')
        # create title
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        op_string = 'comments and links' if operation == 'all' else operation
        title = f'{ticker.upper()} on r/{subreddit} ({op_string}). Current Time: {dt_string}'
        plt.suptitle(title, fontweight='bold')
        # subplot titles
        self.axes[0].title.set_text(f'{ticker.upper()} Close Price')
        self.axes[1].title.set_text(f'r/{subreddit} Mentions')
        self.axes[2].title.set_text(f'Score of Mentions')

    def graphTickerAndSubredditData(self, subredditDataForPeriod, tickerHistoryForPeriod, operation):

        # show markers for mentions and score if <= than this # of data points
        markerLimit = 15
        # show averages if more than this # of of data points for mentions and scores
        # close price is always shown
        movingAverageLimit = 50

        # plot mentions
        if ( operation in ['links', 'all'] ):
            totalLinks = subredditDataForPeriod['Links'].sum()
            if ( len(subredditDataForPeriod.index) >= movingAverageLimit  ):
                subredditDataForPeriod['LMA50'] = subredditDataForPeriod['Links'].rolling(25).mean()
                subredditDataForPeriod['LMA50'].plot(ax=self.axes[1], style='c-', label=f'Links MA25 ({totalLinks} Total)')  
            else:
                if ( len(subredditDataForPeriod.index) > markerLimit ):
                    subredditDataForPeriod['Links'].plot(ax=self.axes[1], style='c-', label=f'Links ({totalLinks} Total)')
                else:
                    subredditDataForPeriod['Links'].plot(ax=self.axes[1], style='c-', marker='o', label=f'Links ({totalLinks} Total)')
        if ( operation in ['comments', 'all'] ):
            # TODO: change from float in df to int, not here
            totalUniqueComments = int(subredditDataForPeriod['Comments'].sum())       
            if ( len(subredditDataForPeriod.index) >= movingAverageLimit  ):
                subredditDataForPeriod['CMA50'] = subredditDataForPeriod['Comments'].rolling(25).mean()
                subredditDataForPeriod['CMA50'].plot(ax=self.axes[1], style='m-', label=f'Comments MA25 ({totalUniqueComments} Total Unique)')
            else:
                if ( len(subredditDataForPeriod.index) > markerLimit ):
                    subredditDataForPeriod['Comments'].plot(ax=self.axes[1], style='m-', label=f'Comments ({totalUniqueComments} Total Unique)')
                else:
                    subredditDataForPeriod['Comments'].plot(ax=self.axes[1], style='m-', marker='o', label=f'Comments ({totalUniqueComments} Total Unique)')
            totalComments = subredditDataForPeriod['Total Comments'].sum()
            self.axes[1].plot([], [], ' ', label=f'{totalComments} Total Comments')

        # plot prices
        if ( len(subredditDataForPeriod.index) > markerLimit ):
            tickerHistoryForPeriod['Close'].plot(ax=self.axes[0], style='r-', label='Close')
        else:
            tickerHistoryForPeriod['Close'].plot(ax=self.axes[0], style='r-', marker='o', label='Close')
        # calculate the rolling average if data set is large enough
        if ( len(subredditDataForPeriod.index) >= movingAverageLimit ):
            tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(25).mean()
            tickerHistoryForPeriod['MA50'].plot(ax=self.axes[0], style='y-', label='MA25')

        # plot scores
        if ( operation in ['links', 'all'] ):
            if ( len(subredditDataForPeriod.index) >= movingAverageLimit  ):
                subredditDataForPeriod['LAMA50'] = subredditDataForPeriod['Links Avg Score'].rolling(25).mean()
                subredditDataForPeriod['LAMA50'].plot(ax=self.axes[2], style='y-', label='Links Avg MA25')
            else:
                if ( len(subredditDataForPeriod.index) > markerLimit ):
                    subredditDataForPeriod['Links Avg Score'].plot(ax=self.axes[2], style='y-', label='Links Average')
                else:
                    subredditDataForPeriod['Links Avg Score'].plot(ax=self.axes[2], style='y-', marker='o', label='Links Average')
        if ( operation in ['comments', 'all'] ):
            if ( len(subredditDataForPeriod.index) >= movingAverageLimit  ):
                subredditDataForPeriod['CMMA50'] = subredditDataForPeriod['Comments Max'].rolling(25).mean()
                subredditDataForPeriod['CMMA50'].plot(ax=self.axes[2], style='b-', label='Comments Max MA25')
            else:
                if ( len(subredditDataForPeriod.index) > markerLimit ):
                    subredditDataForPeriod['Comments Max'].plot(ax=self.axes[2], style='b-', label='Max Comment')    
                else:
                    subredditDataForPeriod['Comments Max'].plot(ax=self.axes[2], style='b-', marker='o', label='Max Comment')

        # grid
        self.axes[0].grid()
        self.axes[1].grid()
        self.axes[2].grid()
        # legend
        self.axes[0].legend(loc='upper right')
        self.axes[1].legend(loc='upper right')
        self.axes[2].legend(loc='upper right')
        # show plots
        plt.show()

        # TODO: allow option to save graph
        #df.to_csv("foo.csv")
