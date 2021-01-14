import yfinance

class FinanceClient:

    def __init__(self):

        print('creating finance client')

    def test(self):

        tsla = yf.Ticker("TSLA")
        print(tsla.info)
