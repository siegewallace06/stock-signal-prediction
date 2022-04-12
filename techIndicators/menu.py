#import required module(s)
from ta.utils import dropna
import yfinance as yf
import os

# import local python file(s)
from . import accDistIndex as ADX
from . import movAvgConvDiv as MACD
# Basic Menu 

def mainMenu() :
    print("Welcome to Stock Simulation Program!")
    stockSymbol = input("Please enter the stock symbol(ticker) : ")
    stockSymbol = stockSymbol.upper()
    #Add .JK for stock symbol in Indonesia Stock Exchange
    stockSymbol = stockSymbol + ".JK"
    #you can use this if you dont want to manually input
    # stockSymbol = "CODE.JK"
    #input the period time for the trading data
    stockPeriod = input("Please enter the period : ")
    #input the interval gap for the trading data
    stockInterval = input("Please enter the interval : ")

    #Download the stock data
    stock = yf.download(stockSymbol, period = stockPeriod, interval = stockInterval)

    # Check if the data frame is empty then repeat
    if stock.empty :
        print("Please enter the correct stock symbol!")
        os.system("pause")
        os.system("cls")
        mainMenu()
    
    print("Stock Data Succesfully Acquired!")
    os.system("pause")
    os.system("cls")

    return stock, stockSymbol


def techIndicatorsMenu(stock) :

    # print(stock)
    # os.system("pause")
    # os.system("cls")

    print("Which Technical Indicator(s) you would you like to add? ", end = "")
    print('''
    1. ADX
    2. MACD
    3. RSI
    4. ATR
    0. Go To Simulation
    ''')

    userChoice = input("Enter your choice : ")
    userChoice = int(userChoice)

    if userChoice == 1 :
        ADX.calculate(stock)
    elif userChoice == 2:
        windowFast = input("Please input n-period short-term(Default period : 12) : ")
        windowFast = int(windowFast)

        windowSlow = input("Please input n-period long-term(Default period : 26) : ")
        windowSlow = int(windowSlow)

        windowSignal = input("Please input n-period to signal(Default period : 9) : ")
        windowSignal = int(windowSignal)

        MACD.calculate(stock,windowFast,windowSlow,windowSignal)
    elif userChoice == 3 :
        pass
    elif userChoice == 4 :
        pass
    elif userChoice == 0 :
        print("")


    # print("PLEASE ENTER A NUMBER!")
    # os.system("pause")
    # os.system("cls")