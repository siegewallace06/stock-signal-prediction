from ta.volume import AccDistIndexIndicator as ADX
from . import menu
import os

def calculate(stock) :
    # Initiate ADX Indicator Variable
    # Parameters :
    # high (pandas.Series) – dataset ‘High’ column.
    # low (pandas.Series) – dataset ‘Low’ column.
    # close (pandas.Series) – dataset ‘Close’ column.
    # volume (pandas.Series) – dataset ‘Volume’ column.
    # fillna (bool) – if True, fill nan values.
    ADXIndicator = ADX(high = stock["High"], low = stock["Low"], close = stock["Close"], volume = stock["Volume"])

    # Add ADX Features to the data frame
    stock["ADX"] = ADXIndicator.acc_dist_index()

    print("The ADX Values and Signal Recommendation has been succesfully added!")
    print("Type anything to return to the menu")
    os.system("continue")

    menu.techIndicatorsMenu(stock)
    return()