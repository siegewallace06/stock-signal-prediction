# Import module for beautiful table
from beautifultable import BeautifulTable

import pandas as pd
import os


def runSimulation(stock,indicatorColumn, signalColumn, stockSymbol):
    # Trading Simulation
    # Declare variable to check if we already owned the stock or not
    isOwned = False
    # Declare variable for storing total profit
    totalProfit = 0
    # Declare variable for storing current closing price on current loop
    currentPrice = 0
    # Declare variable for storing how much we purchased the stock
    numberPurchase = 0
    # Declare variable for storing how much we sell the stock
    numberSell = 0
    # Declare variable for storing initial Capital price
    initialCapital = 0
    # Declare variable for storing total tax we payed
    totalTax = 0
    # Declare variable for storing how many loop that we did
    i = 0

    # Create list for the dictionary later
    indexList = list()
    closePriceList = list()
    taxList = list()
    orderList = list()
    purchasedPriceList = list()
    profitList = list()
    signalList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))

    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[signalColumn] == "BUY":
                orderList.append("BUY")
                signalList.append(row[indicatorColumn])
                # assign the current price
                currentPrice = row["Close"] * 100
                closePriceList.append(currentPrice)
                # Calculate the tax
                tax = currentPrice * 0.36 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax
                # Calculate total buy price
                buyPrice = currentPrice + tax
                purchasedPriceList.append(buyPrice)
                profitList.append(0)
                # Check if initial capital is 0 then assign the buy price to the initialCapital variable
                if initialCapital == 0:
                    initialCapital = buyPrice
                # Change the boolean to True, to indicate we already own the stock
                isOwned = True
                # add one to the number purchased
                numberPurchase = numberPurchase + 1
                # Test print
                # print(i,". Buy Counter :",numberPurchase," Purchased at Rp.",currentPrice)
                # print("Rp.",totalProfit)
                i = i + 1
                indexList.append(i)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[signalColumn] == "SELL":
                orderList.append("SELL")
                signalList.append(row[indicatorColumn])
                # Temp variable to store the current price
                tempPrice = row["Close"] * 100
                closePriceList.append(tempPrice)
                # calculate the tax
                tax = tempPrice * 0.46 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax
                # Calculate total sell price
                sellPrice = tempPrice - tax
                purchasedPriceList.append(buyPrice)
                # calc the profit by subtract it with the purchase value
                profit = sellPrice - buyPrice
                profitList.append(profit)
                # add to total profit
                totalProfit = totalProfit + profit
                # Change the boolean to False, to indicate that we don't own the stock anymore
                isOwned = False
                numberSell = numberSell + 1
                # test print
                # print(i,". Sell Counter :",numberSell," Sold at Rp.",tempPrice)
                # print("Rp.",totalProfit)
                i = i + 1
                indexList.append(i)
    # print("Total Profit : Rp.",totalProfit)

    simulationLogDict = {"Close Price": closePriceList,
                         "Tax": taxList,
                         "Purchased Price" : purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         indicatorColumn : signalList
                         }

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Index", "Close Price", "Tax", "Purchased Price", "Capital Gain", "Order", indicatorColumn]
    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i], signalList[i]])
        i = i + 1
    # simulationTable.columns.insert(indexList, header = "Index")
    # simulationTable.columns.insert(closePriceList, header = "Close Price")
    # simulationTable.columns.insert(purchasedPriceList, header = "Purchased Price")
    # simulationTable.columns.insert(profitList, header="Profit")
    # simulationTable.columns.insert(orderList,header="Order")
    print(simulationTable)

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationLog.to_csv("Log/" + stockSymbol + ".csv")

    # SIMULATION SUMMARY
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)

    print("--------------------------")
    print("SIMULATION SUMMARY")
    print("--------------------------")
    print("Initial Capital : Rp.", initialCapital)
    print("Total Capital Gain : Rp.", totalProfit, "(", profitPercentage, "%)")
    print("Total Transaction Fee Paid : Rp.", totalTax)
    print("Number of stock(s) purchased: ", numberPurchase)
    print("Number of stock(s) sold : ", numberSell)

    print("\nSimulation Success and log printed to CSV! Type anything to return to the Simulation Menu")
    os.system("pause")
