# Import DC Class
from ta.volatility import DonchianChannel as DC

def calculate(stock, window) :
   # Initiate DC Indicator Variable
    # Parameters
    # high (pandas.Series) – dataset ‘High’ column.
    # low (pandas.Series) – dataset ‘Low’ column.
    # close (pandas.Series) – dataset ‘Close’ column.
    # window (int) – n period (Default 20 days). 
    # fillna (bool) – if True, fill nan values.
    DCIndicator = DC(high = stock["High"], low = stock["Low"], close = stock["Close"], window = 20 )

    # Add DC Features to the dataframe
    stock["DC_hband"] = DCIndicator.donchian_channel_hband()
    stock["DC_mband"] = DCIndicator.donchian_channel_mband()
    stock["DC_lband"] = DCIndicator.donchian_channel_lband()
    #I still don't know the usage of percentage and width band, further research required
    # stock["DC_pband"] = DCIndicator.donchian_channel_pband()
    # stock["DC_wband"] = DCIndicator.donchian_channel_wband()

    # How To Identify The Signal
    # IF the closing price EQUAL or MORE than High Band or Higher than Mid Band THEN SELL
    # IF the closing price EQUAL or LESS than Low Band or Less than Mid Band THEN BUY

    stock.loc[(stock['Close'] >= stock['DC_hband']) , 'DC_Signal'] = 'SELL'
    stock.loc[(stock['Close'] >= stock['DC_mband']) , 'DC_Signal'] = 'SELL'
    stock.loc[(stock['Close'] <= stock['DC_mband']) , 'DC_Signal'] = 'BUY'
    stock.loc[(stock['Close'] <= stock['DC_mband']) , 'DC_Signal'] = 'BUY'