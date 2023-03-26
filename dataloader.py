import yfinance as yf
import pandas as pd
import nasdaqdatalink


class DataLoader:
    def __init__(self, tickers, dates):
        self.dates = dates
        self.tickers = {ticker: self._prepare_ticker(
            ticker) for ticker in tickers}
        self._prepare_world_data()
        self._merge_world_and_ticker()

    def _prepare_ticker(self, tickerSymbol):
        tickerData = yf.Ticker(tickerSymbol)
        df = tickerData.history(
            interval='1d', start=self.dates[0], end=self.dates[1])
        df.drop(['Dividends', 'Stock Splits', 'Capital Gains'],
                axis=1, inplace=True)

        df['Rolling5dHigh'] = df['High'].shift(1).rolling(5).max()
        df['Rolling5dLow'] = df['Low'].shift(1).rolling(5).min()
        df['Expon5dCloseAverage'] = df['Close'].shift(1).ewm(5).mean()
        df['Expon1mCloseAverage'] = df['Close'].shift(1).ewm(30).mean()
        df['Expon6mCloseAverage'] = df['Close'].shift(1).ewm(30*6).mean()
        df = df.drop(columns=['Open', 'High', 'Low'])
        df = df[df.index.isocalendar().day.isin([1, 5])]
        df.dropna(inplace=True)

        df['Month'] = pd.DatetimeIndex(df.index).month
        df['Year'] = pd.DatetimeIndex(df.index).year
        return df

    def _prepare_world_data(self, data_paths=['FRED/MEDCPIM158SFRBCLE', 'FRED/FEDFUNDS'],
                            data_names=['CPI', '10YInterest'], dates=['2009-1-1', '2013-12-31']):
        self.world_data = []
        for d, n in zip(data_paths, data_names):
            df = nasdaqdatalink.get(d, start_date=dates[0], end_date=dates[1])
            df = df.rename(columns={'Value': n})
            df['Month'] = pd.DatetimeIndex(df.index).month
            df['Year'] = pd.DatetimeIndex(df.index).year
            self.world_data.append(df)

    def _merge_world_and_ticker(self):
        self.data = self.tickers
        for df in self.world_data:
            self.data = {ticker: pd.merge(dataframe, df,
                                          on=['Month', 'Year'], how='inner')
                         for ticker, dataframe in self.data.items()
                         }
