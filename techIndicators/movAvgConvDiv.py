import os

# import MACD class from ta module
from ta.trend import MACD

def calculate(stock,windowFast,windowSlow,windowSignal) :
    # Initialize MACD variable
    # parameters
    # close (pandas.Series) – dataset ‘Close’ column.
    # window_fast (int) – n period short-term.
    # window_slow (int) – n period long-term.
    # window_sign (int) – n period to signal.
    # fillna (bool) – if True, fill nan values.
    MACDIndicator = MACD(stock['Close'],window_fast = windowFast, window_slow = windowSlow, window_sign = windowSignal)

    # Add MACD features to the data frame
    stock['MACD_line'] = MACDIndicator.macd()
    stock["MACD_histogram"] = MACDIndicator.macd_diff()
    stock['MACD_signal'] = MACDIndicator.macd_signal()

    # How We Indentify The Signal
    # IF the MACD_line is Positive AND the MACD_signal collides with the signal THEN it's time to SELL
    # IF the MACD line is Negative AND the MACD_signal collides with the signal THEN it's time to BUY

    # in the dataframe, locate the column that are correct according to the rules above.
    # after that assign the signal to MACD_Recommend
    # For now the 'HOLD' is just a placeholder so the column won't be empty
    stock.loc[(stock['MACD_line'] >= 1) & (stock['MACD_line']  >= stock['MACD_signal']), 'MACD_Recommend'] = 'SELL'
    stock.loc[(stock['MACD_line'] >= 1) & (stock['MACD_line']  <= stock['MACD_signal']), 'MACD_Recommend'] = 'HOLD'

    stock.loc[(stock['MACD_line'] <= 0) & (stock['MACD_line']  <= stock['MACD_signal']), 'MACD_Recommend'] = 'BUY'
    stock.loc[(stock['MACD_line'] <= 0) & (stock['MACD_line']  >= stock['MACD_signal']), 'MACD_Recommend'] = 'HOLD'

    print("The MACD Values and Signal Recommendation has been succesfully added!")
    print("Type anything to return to the menu")
    os.system("continue")