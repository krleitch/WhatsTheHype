import yfinance as yf

class FinanceClient:

    def __init__(self, ticker):
        self.tickerData = yf.Ticker(ticker)

    def getTickerHistoryForPeriod(self, period):

        if (period == 'day' ):
            return self.tickerData.history(period="1d")
        elif (period == 'week'):
            return self.tickerData.history(period="7d")
        elif (period == 'biweek'):
            return self.tickerData.history(period="14d")
        elif (period == 'month'):
            return self.tickerData.history(period="1mo")
        elif (period == 'quarter'):
            return self.tickerData.history(period="3mo")
        elif (period == 'half'):
            return self.tickerData.history(period="6mo")
        elif (period == 'year'):
            return self.tickerData.history(period="1y")
        else:
            return self.tickerData.history(period="max")
