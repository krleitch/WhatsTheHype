import yfinance as yf

class FinanceClient:

    def __init__(self, ticker):
        self.tickerData = yf.Ticker(ticker)

    def getTickerHistoryForPeriod(self, before, after):

        # TODO: we just ignore all the data after the 'before' right now

        period = str(after) + 'd'
        return self.tickerData.history(period=period)

