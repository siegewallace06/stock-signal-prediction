# Import ATR Class
from ta.volatility import AverageTrueRange as ATR

def calculate(stock, window) :
    # Initiate ATR Indicator Variable
    # Parameters
    # high (pandas.Series) – dataset ‘High’ column.
    # low (pandas.Series) – dataset ‘Low’ column.
    # close (pandas.Series) – dataset ‘Close’ column.
    # window (int) – n period.
    # fillna (bool) – if True, fill nan values.
    ATRIndicator = ATR(high = stock["High"], low = stock["Low"], close = stock["Close"], window = window )

    # Add ATR column to the dataframe
    stock["ATR"] = ATRIndicator.average_true_range()