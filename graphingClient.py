import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self):

        plt.close("all")

    def graphTickerAndHistory(self, subredditTickerCount, tickerHistory):

        # rolling average
        tickerHistory['MA50'] = tickerHistory['Close'].rolling(50).mean()
        tickerHistory[['Close', 'MA50']].plot(label='count', figsize=(16,8), title="Mentions")
        plt.legend()
        plt.show()

        # save graph
        #df.to_csv("foo.csv")
