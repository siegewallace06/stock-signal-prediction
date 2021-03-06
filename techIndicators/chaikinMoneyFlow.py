from ta.volume import ChaikinMoneyFlowIndicator as CMF
from . import menu
import os

def calculate(stock,window) :
    # Initiate CMF Indicator Variable
    # Parameters
    # high (pandas.Series) – dataset ‘High’ column.
    # low (pandas.Series) – dataset ‘Low’ column.
    # close (pandas.Series) – dataset ‘Close’ column.
    # volume (pandas.Series) – dataset ‘Volume’ column.
    # window (int) – n period (Default : 20 Period).
    # fillna (bool) – if True, fill nan values.
    CMFIndicator = CMF(high = stock["High"], low = stock["Low"], close = stock["Close"], volume = stock["Volume"],window = window)


    # Add CMF Features to the data frame
    stock["CMF"] = CMFIndicator.chaikin_money_flow()

    stock.loc[stock['CMF'] > 0, 'CMF_Recommend'] = 'BUY'
    stock.loc[stock['CMF'] < 0, 'CMF_Recommend'] = 'SELL'

    print("The CMF Values and Signal Recommendation has been succesfully added!")
    print("Type anything to return to the menu")
    os.system("pause")

    # menu.techIndicatorsMenu(stock)
    return()