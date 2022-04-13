import os

# import RSI module
from ta.momentum import RSIIndicator as RSI

def calculate(stock, window = 14):
    # Initiate RSI Indicator Variable
    # Parameters
    # close (pandas.Series) – dataset ‘Close’ column.
    # window (int) – n period
    # fillna (bool) – if True, fill nan values.
    RSIIndicators = RSI(stock['Close'], window = window)

    # Add RSI Column to the data frame
    stock['RSI'] = RSIIndicators.rsi()

    #How we identify the signal with RSI
    # If RSI Value is between 0 and 30 then the current condition is OVERSOLD and the signal is BUY
    # If RSI value is between 70 and 100 then the current condition is OVERBOUGHT and the signal is SELL
    # If the RSI value between 31 and 69 we will do nothing or HOLD
    stock.loc[(stock['RSI'] >= 0) & (stock['RSI']  <= 30), 'RSI_Recommend'] = 'BUY'
    stock.loc[(stock['RSI'] >= 31) & (stock['RSI']  <= 69), 'RSI_Recommend'] = 'HOLD'
    stock.loc[(stock['RSI'] >= 70) & (stock['RSI']  <= 100), 'RSI_Recommend'] = 'SELL'

    
    print("The RSI Values and Signal Recommendation has been succesfully added!")
    print("Type anything to return to the menu")
    os.system("pause")