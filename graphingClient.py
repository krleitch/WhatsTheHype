import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphingClient:

    def __init__(self):

        print('creating graphing client')
        plt.close("all")

    def test(self, hist):

        # print(hist.keys())
        hist['Close'].plot(label='TEST', figsize=(16,8), title="test")
        plt.legend()
        plt.show()
        #df.to_csv("foo.csv")
