'''
Python Script for Creating Trade Signal from various technical indicators
Author : R

To learn how to use the script go to ReadMe File

Version 1.00
'''
# import all required python file(s)
from techIndicators import menu

stock, stockSymbol = menu.mainMenu()

stockSymbol = stockSymbol[0:4]

# print(stock)

menu.techIndicatorsMenu(stock)

print(stock)
print(type(stock))