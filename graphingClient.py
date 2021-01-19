import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self):
        plt.close("all")

    def graphTickerAndHistory(self, subredditMentions, tickerHistoryForPeriod):

        # rolling average
        tickerHistoryForPeriod['MA50'] = tickerHistoryForPeriod['Close'].rolling(50).mean()
        # close price
        tickerHistoryForPeriod[['Close', 'MA50']].plot(label='stock', figsize=(16,8), title="Stock Vs Mentions")
        # mentions
        subredditMentions.plot(label='mentions')
        plt.legend()
        plt.show()

        # save graph
        #df.to_csv("foo.csv")
