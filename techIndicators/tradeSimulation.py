# Import module for beautiful table
from beautifultable import BeautifulTable

import pandas as pd
import os


def runSimulation(stock, indicatorColumn, signalColumn, stockSymbol, indicatorColumn2=None, indicatorColumn3=None):
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

    if indicatorColumn3 != None:
        signalList3 = list()
        signalList2 = list()
    elif indicatorColumn2 != None:
        signalList2 = list()
    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))

    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[signalColumn] == "BUY":
                orderList.append("BUY")
                signalList.append(row[indicatorColumn])
                if indicatorColumn3 != None:
                    signalList3.append(row[indicatorColumn3])
                if indicatorColumn2 != None:
                    signalList2.append(row[indicatorColumn2])
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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[signalColumn] == "SELL":
                orderList.append("SELL")
                signalList.append(row[indicatorColumn])
                if indicatorColumn3 != None:
                    signalList3.append(row[indicatorColumn3])
                if indicatorColumn2 != None:
                    signalList2.append(row[indicatorColumn2])
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
                indexList.append(index)
    # print("Total Profit : Rp.",totalProfit)

    if indicatorColumn3 != None:
        simulationLogDict = {"Date": indexList,
                             "Close Price": closePriceList,
                             "Fee": taxList,
                             "Purchased Price": purchasedPriceList,
                             "Capital Gain": profitList,
                             "Order": orderList,
                             indicatorColumn: signalList,
                             indicatorColumn2: signalList2,
                             indicatorColumn3: signalList3
                             }
    elif indicatorColumn2 != None:
        simulationLogDict = {"Date": indexList,
                             "Close Price": closePriceList,
                             "Fee": taxList,
                             "Purchased Price": purchasedPriceList,
                             "Capital Gain": profitList,
                             "Order": orderList,
                             indicatorColumn: signalList,
                             indicatorColumn2: signalList2
                             }
    else:
        simulationLogDict = {"Date": indexList,
                             "Close Price": closePriceList,
                             "Fee": taxList,
                             "Purchased Price": purchasedPriceList,
                             "Capital Gain": profitList,
                             "Order": orderList,
                             indicatorColumn: signalList
                             }
    simulationTable = BeautifulTable()

    # print(len(signalList))
    # print(len(signalList2))
    # print(len(signalList3))

    if indicatorColumn3 != None:
        simulationTable.columns.header = [
            "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", indicatorColumn, indicatorColumn2, indicatorColumn3]
        i = 0
        while i < len(indexList):
            simulationTable.rows.append(
                [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i], signalList[i], signalList2[i], signalList3[i]])
            i = i + 1
    elif indicatorColumn2 != None:
        simulationTable.columns.header = [
            "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", indicatorColumn, indicatorColumn2]
        i = 0
        while i < len(indexList):
            simulationTable.rows.append(
                [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i], signalList[i], signalList2[i]])
            i = i + 1

    else:
        simulationTable.columns.header = [
            "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", indicatorColumn]
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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    indicatorColumnList = list()
    indicatorColumnList.append(indicatorColumn)

    simulationSummaryDict = {
        "Initial Capital": initialCapital,
        "Total Capital Gain": totalProfit,
        "Capital Gain Percentage": profitPercentage,
        "Transaction Fee": totalTax,
        "Number Purchased": numberPurchase,
        "Number Sold": numberSell,
        "Indicator": indicatorColumn
    }

    # summaryTemp = pd.DataFrame(simulationSummaryDict)
    simulationSummary = pd.read_csv("Log/Summary/summary.csv")
    simulationSummary.append(simulationSummaryDict, ignore_index=True)

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorColumn + ".csv"

    simulationLog.to_csv(simulationPath)

    print("\nSimulation Success and log printed to", simulationPath,
          "! Type anything to return to the Simulation Menu")
    os.system("pause")


def cmf_macd(stock, stockSymbol):
    cmfColumn = "CMF"
    cmfSignal = "CMF_Recommend"

    macdLine = "MACD_line"
    macdHist = "MACD_histogram"
    macdSig = "MACD_signal"
    macdSignal = "MACD_Recommend"

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

    cmfColumnList = list()

    macdLineList = list()
    macdHistList = list()
    macdSignList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[cmfSignal] == "BUY" and row[macdSignal] == "BUY":
                orderList.append("BUY")

                cmfColumnList.append(row[cmfColumn])

                macdLineList.append(row[macdLine])
                macdHistList.append(row[macdHist])
                macdSignList.append(row[macdSig])

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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[cmfSignal] == "SELL" and row[macdSignal] == "SELL":
                orderList.append("SELL")

                cmfColumnList.append(row[cmfColumn])

                macdLineList.append(row[macdLine])
                macdHistList.append(row[macdHist])
                macdSignList.append(row[macdSig])

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
                indexList.append(index)

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", cmfColumn, macdLine, macdHist, macdSig]

    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i], cmfColumnList[i], macdLineList[i], macdHistList[i], macdSignList[i]])
        i = i + 1

    print(simulationTable)

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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    # indicatorColumnList = list()
    # indicatorColumnList.append(indicatorColumn)


    simulationLogDict = {"Date": indexList,
                         "Close Price": closePriceList,
                         "Fee": taxList,
                         "Purchased Price": purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         cmfColumn: cmfColumnList,
                         macdLine: macdLineList,
                         macdHist: macdHistList,
                         macdSig: macdSignList
                         }

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + "CMF_MACD" + ".csv"

    simulationLog.to_csv(simulationPath)
    os.system("pause")

def cmf_dc(stock,stockSymbol):

    cmfColumn = "CMF"
    cmfSignal = "CMF_Recommend"

    dcHband = "DC_hband"
    dcMband = "DC_mband"
    dcLband = "DC_lband"
    dcSignal = "DC_Recommend"

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

    cmfColumnList = list()

    dcHbandList = list()
    dcMbandList = list()
    dcLbandList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[cmfSignal] == "BUY" and row[dcSignal] == "BUY":
                orderList.append("BUY")

                cmfColumnList.append(row[cmfColumn])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[cmfSignal] == "SELL" and row[dcSignal] == "SELL":
                orderList.append("SELL")

                cmfColumnList.append(row[cmfColumn])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", cmfColumn, dcHband, dcMband, dcLband]

    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i], cmfColumnList[i], dcHbandList[i], dcMbandList[i], dcLbandList[i]])
        i = i + 1

    print(simulationTable)

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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    # indicatorColumnList = list()
    # indicatorColumnList.append(indicatorColumn)

    simulationLogDict = {"Date": indexList,
                         "Close Price": closePriceList,
                         "Fee": taxList,
                         "Purchased Price": purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         cmfColumn: cmfColumnList,
                         dcHband: dcHbandList,
                         dcMband: dcMbandList,
                         dcLband: dcLbandList
                         }

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + "CMF_DC" + ".csv"

    simulationLog.to_csv(simulationPath)




def rsi_cmf_macd(stock,stockSymbol):

    rsiColumn = "RSI"
    rsiSignal = "RSI_Recommend"

    cmfColumn = "CMF"
    cmfSignal = "CMF_Recommend"

    macdLine = "MACD_line"
    macdHist = "MACD_histogram"
    macdSig = "MACD_signal"
    macdSignal = "MACD_Recommend"

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

    rsiColumnList = list()
    rsiSignalList = list()

    cmfColumnList = list()

    macdLineList = list()
    macdHistList = list()
    macdSignList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[rsiSignal] == "BUY" and row[cmfSignal] == "BUY" and row[macdSignal] == "BUY":
                orderList.append("BUY")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                macdLineList.append(row[macdLine])
                macdHistList.append(row[macdHist])
                macdSignList.append(row[macdSig])

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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[rsiSignal] == "SELL" and row[cmfSignal] == "SELL" and row[macdSignal] == "SELL":
                orderList.append("SELL")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                macdLineList.append(row[macdLine])
                macdHistList.append(row[macdHist])
                macdSignList.append(row[macdSig])

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
                indexList.append(index)

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", rsiColumn, cmfColumn, macdLine, macdHist, macdSig]

    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i],rsiColumnList[i], cmfColumnList[i], macdLineList[i], macdHistList[i], macdSignList[i]])
        i = i + 1

    print(simulationTable)

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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    # indicatorColumnList = list()
    # indicatorColumnList.append(indicatorColumn)

    simulationLogDict = {"Date": indexList,
                         "Close Price": closePriceList,
                         "Fee": taxList,
                         "Purchased Price": purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         cmfColumn: cmfColumnList,
                         macdLine: macdLineList,
                         macdHist: macdHistList,
                         macdSig: macdSignList
                         }

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + "RSI_CMF_MACD" + ".csv"

    simulationLog.to_csv(simulationPath)

    os.system("pause")


def rsi_cmf_dc(stock,stockSymbol):

    rsiColumn = "RSI"
    rsiSignal = "RSI_Recommend"

    cmfColumn = "CMF"
    cmfSignal = "CMF_Recommend"

    dcHband = "DC_hband"
    dcMband = "DC_mband"
    dcLband = "DC_lband"
    dcSignal = "DC_Recommend"

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

    rsiColumnList = list()
    rsiSignalList = list()

    cmfColumnList = list()

    dcHbandList = list()
    dcMbandList = list()
    dcLbandList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[rsiSignal] == "BUY" and row[cmfSignal] == "BUY" and row[dcSignal] == "BUY":
                orderList.append("BUY")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[rsiSignal] == "SELL" and row[cmfSignal] == "SELL" and row[dcSignal] == "SELL":
                orderList.append("SELL")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", rsiColumn, cmfColumn, dcHband, dcMband, dcLband]

    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i],rsiColumnList[i], cmfColumnList[i], dcHbandList[i], dcMbandList[i], dcLbandList[i]])
        i = i + 1

    print(simulationTable)

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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    # indicatorColumnList = list()
    # indicatorColumnList.append(indicatorColumn)

    simulationLogDict = {"Date": indexList,
                         "Close Price": closePriceList,
                         "Fee": taxList,
                         "Purchased Price": purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         cmfColumn: cmfColumnList,
                         dcHband: dcHbandList,
                         dcMband: dcMbandList,
                         dcLband: dcLbandList
                         }

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + "RSI_CMF_DC" + ".csv"

    simulationLog.to_csv(simulationPath)

    os.system("pause")
    
def rsi_cmf_macd_dc(stock,stockSymbol):

    rsiColumn = "RSI"
    rsiSignal = "RSI_Recommend"

    cmfColumn = "CMF"
    cmfSignal = "CMF_Recommend"

    macdLine = "MACD_line"
    macdHist = "MACD_histogram"
    macdSig = "MACD_signal"
    macdSignal = "MACD_Recommend"

    dcHband = "DC_hband"
    dcMband = "DC_mband"
    dcLband = "DC_lband"
    dcSignal = "DC_Recommend"

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

    rsiColumnList = list()
    rsiSignalList = list()

    macdLineList = list()
    macdHistList = list()
    macdSignList = list()

    cmfColumnList = list()

    dcHbandList = list()
    dcMbandList = list()
    dcLbandList = list()

    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # use itterows method to iterate the Data Frame
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[rsiSignal] == "BUY" and row[cmfSignal] == "BUY" and row[macdSignal] == "BUY" and row[dcSignal] == "BUY":
                orderList.append("BUY")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                macdLineList.append(row[macdLine])
                macdHistList.append(row[macdHist])
                macdSignList.append(row[macdSig])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[rsiSignal] == "SELL" and row[cmfSignal] == "SELL" and row[macdSignal] == "SELL" and row[dcSignal] == "SELL":
                orderList.append("SELL")

                rsiColumnList.append(row[rsiColumn])

                cmfColumnList.append(row[cmfColumn])

                dcHbandList.append(row[dcHband])
                dcMbandList.append(row[dcMband])
                dcLbandList.append(row[dcLband])

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
                indexList.append(index)

    simulationTable = BeautifulTable()
    simulationTable.columns.header = [
        "Date", "Close Price", "Fee", "Purchased Price", "Capital Gain", "Order", rsiColumn, macdLine, macdHist, macdSig, cmfColumn, dcHband, dcMband, dcLband]

    i = 0
    while i < len(indexList):
        simulationTable.rows.append(
            [indexList[i], closePriceList[i], taxList[i], purchasedPriceList[i], profitList[i], orderList[i],rsiColumnList[i], macdLineList[i], macdHistList[i], macdSignList[i], cmfColumnList[i], dcHbandList[i], dcMbandList[i], dcLbandList[i]])
        i = i + 1

    print(simulationTable)

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

    initialCapitalList = list()
    initialCapitalList.append(initialCapital)
    totalProfitList = list()
    totalProfitList.append(totalProfit)
    profitPercentageList = list()
    profitPercentageList.append(profitPercentage)
    totalTaxList = list()
    totalTaxList.append(totalTax)
    numberPurchaseList = list()
    numberPurchaseList.append(numberPurchase)
    numberSellList = list()
    numberSellList.append(numberSell)
    # indicatorColumnList = list()
    # indicatorColumnList.append(indicatorColumn)

    simulationLogDict = {"Date": indexList,
                         "Close Price": closePriceList,
                         "Fee": taxList,
                         "Purchased Price": purchasedPriceList,
                         "Capital Gain": profitList,
                         "Order": orderList,
                         cmfColumn: cmfColumnList,
                         macdLine: macdLineList,
                         macdHist: macdHistList,
                         macdSig: macdSignList,
                         dcHband: dcHbandList,
                         dcMband: dcMbandList,
                         dcLband: dcLbandList
                         }

    simulationLog = pd.DataFrame(simulationLogDict)
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + "RSI_CMF_MACD_DC" + ".csv"

    simulationLog.to_csv(simulationPath)
    os.system("pause")
