#import required module(s)
from ta.utils import dropna
import yfinance as yf
import os

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


    STOCK = yf.download(stockSymbol, period = stockPeriod, interval = stockInterval)

    if STOCK.empty :
        print("Please enter the correct stock symbol!")
        os.system("pause")
        os.system("cls")
        mainMenu()
    
    print(STOCK)

    print("Stock Data Succesfully Acquired!")
    os.system("pause")
    os.system("cls")