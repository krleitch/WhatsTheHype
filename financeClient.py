import yfinance as yf

class FinanceClient:

    def __init__(self):
        pass

    def getTickerHistory(self, ticker):

        tsla = yf.Ticker(ticker)
        return tsla.history(period="max")
