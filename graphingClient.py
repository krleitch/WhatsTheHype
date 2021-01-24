import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self):
        # plt configuration
        plt.close("all")
        self.fig, self.axes = plt.subplots(nrows=1, ncols=2, sharex=True)
        self.fig.set_size_inches(10, 5)
        self.axes[0].set_ylabel('Close Price (USD) ')
        self.axes[1].set_ylabel('Mentions')
        plt.suptitle("Stock Vs Mentions")

    def graphTickerAndHistory(self, subredditMentions, tickerHistoryForPeriod):

        # rolling average
        tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(50).mean()
        # close price
        tickerHistoryForPeriod[['Close', 'MA50']].plot(label='stock', ax=self.axes[0])
        # mentions
        subredditMentions['mentions'].plot(label='mentions', ax=self.axes[1])
        plt.legend()
        plt.show()

        # TODO: save graph
        #df.to_csv("foo.csv")
