import yfinance as yf

class FinanceClient:

    def __init__(self):

        print('creating finance client')

    def test(self):

        tsla = yf.Ticker("TSLA")
        hist = tsla.history(period="max")
        return hist
