# import required module(s)
import pandas as pd
from ta.utils import dropna
import yfinance as yf
import os

# ta module reference
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/
# import local python file(s)

from . import chaikinMoneyFlow as CMF
from . import movAvgConvDiv as MACD
from . import relativeStrengthIndex as RSI
from . import donchianChannel as DC
from . import tradeSimulation as simulation
# Basic Menu


def mainMenu():
    print("Welcome to Stock Simulation Program!")
    stockSymbol = input("Please enter the stock symbol(ticker) : ")
    # you can use this if you dont want to manually input
    # stockSymbol = "ARTO"
    stockSymbol = stockSymbol.upper()
    # Add .JK for stock symbol in Indonesia Stock Exchange
    # stockSymbol = stockSymbol + ".JK"

    # input the period time for the trading data
    stockPeriod = input("Please enter the period : ")
    # stockPeriod = "2y"
    # input the interval gap for the trading data
    stockInterval = input("Please enter the interval : ")
    # stockInterval = "1h"

    # Download the stock data
    stock = yf.download(stockSymbol + ".JK",
                        period=stockPeriod, interval=stockInterval)

    # stock = pd.read_csv('Log/Data/FREN.csv')
    #stockSymbol = "FREN"

    # Check if the data frame is empty then repeat
    if stock.empty:
        print("Please enter the correct stock symbol!")
        os.system("pause")
        os.system("cls")
        mainMenu()

    print("Stock Data Succesfully Acquired!")
    os.system("pause")
    os.system("cls")

    return stock, stockSymbol


def techIndicatorsMenu(stock,stockSymbol):

    # print(stock)
    # os.system("pause")
    # os.system("cls")

    print("Which Technical Indicator(s) you would you like to add? ", end="")
    print('''
    1. CMF(Chaikin Money Flow)
    2. MACD(Moving Average Convergence Divergence)
    3. RSI(Relative Strength Index)
    4. DC(Donchian Channel)
    0. Go To Simulation
    ''')

    userChoice = input("Enter your choice : ")
    userChoice = int(userChoice)

    # CHOICE 1 DONE!
    if userChoice == 1:
        window = input("please input n-period(Default period : 20) : ")
        window = int(window)
        CMF.calculate(stock, window)
        os.system("cls")
        techIndicatorsMenu(stock,stockSymbol)

    # CHOICE 2 DONE!
    elif userChoice == 2:
        windowFast = input(
            "Please input n-period short-term(Default period : 12) : ")
        windowFast = int(windowFast)

        windowSlow = input(
            "Please input n-period long-term(Default period : 26) : ")
        windowSlow = int(windowSlow)

        windowSignal = input(
            "Please input n-period to signal(Default period : 9) : ")
        windowSignal = int(windowSignal)

        MACD.calculate(stock, windowFast, windowSlow, windowSignal)
        os.system("cls")
        techIndicatorsMenu(stock,stockSymbol)

    # CHOICE 3 DONE
    elif userChoice == 3:
        window = input("please input n-period(Default period : 14) : ")
        window = int(window)

        RSI.calculate(stock, window)
        os.system("cls")
        techIndicatorsMenu(stock,stockSymbol)

    elif userChoice == 4:
        window = input("please input n-period(Default period : 20) : ")
        window = int(window)

        DC.calculate(stock, window)
        os.system("cls")
        techIndicatorsMenu(stock,stockSymbol)
    elif userChoice == 0:
        dataPath = "Log/Data/" + stockSymbol + ".csv"
        stock.to_csv(dataPath)
        print("Saving and going to simulation menu...")
        os.system("cls")


def simulationMenu(stock, stockSymbol):
    print("Which Technical Indicator(s) would you like to do the simulation? ", end="")
    print('''
    1. CMF(Chaikin Money Flow)
    2. MACD(Moving Average Convergence Divergence)
    3. RSI(Relative Strength Index)
    4. DC(Donchian Channel)
    5. CMF + MACD
    6. CMF + DC
    7. RSI + CMF + MACD
    8. RSI + CMF + DC
    9. RSI + CMF + MACD + DC
    0. Exit
    ''')


    userChoice = input("Enter your choice : ")
    userChoice = int(userChoice)

    # CHOICE 1 DONE!
    if userChoice == 1:
        signalColumn = "CMF_Recommend"
        indicatorColumn = "CMF"
        simulation.runSimulation(
            stock, indicatorColumn, signalColumn, stockSymbol)
        simulationMenu(stock, stockSymbol)
    #CHOICE 2 DONE!
    elif userChoice == 2:
        signalColumn = "MACD_Recommend"
        indicatorColumn = "MACD_line"
        indicatorColumn2 = "MACD_histogram"
        indicatorColumn3 = "MACD_signal"
        simulation.runSimulation(stock, indicatorColumn, signalColumn, stockSymbol,
                                 indicatorColumn2=indicatorColumn2, indicatorColumn3=indicatorColumn3)
        simulationMenu(stock, stockSymbol)

    # CHOICE 3 DONE!
    elif userChoice == 3:
        signalColumn = "RSI_Recommend"
        indicatorColumn = "RSI"
        simulation.runSimulation(
            stock, indicatorColumn, signalColumn, stockSymbol)
        simulationMenu(stock, stockSymbol)
    
    elif userChoice == 4:
        signalColumn = "DC_Recommend"
        indicatorColumn = "DC_hband"
        indicatorColumn2 = "DC_mband"
        indicatorColumn3 = "DC_lband"
        simulation.runSimulation(stock, indicatorColumn, signalColumn, stockSymbol,
                                 indicatorColumn2=indicatorColumn2, indicatorColumn3=indicatorColumn3)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 5:
        simulation.cmf_macd(stock,stockSymbol)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 6 :
        simulation.cmf_dc(stock,stockSymbol)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 7 :
        simulation.rsi_cmf_macd(stock,stockSymbol)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 8 :
        simulation.rsi_cmf_dc(stock,stockSymbol)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 9 :
        simulation.rsi_cmf_macd_dc(stock,stockSymbol)
        simulationMenu(stock, stockSymbol)
    elif userChoice == 0:
        exit()
