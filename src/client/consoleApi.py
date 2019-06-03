import Input.bm_input as bm_input
import Utils.sad as sad
import json

def initConsole():
    print("Binance Manager")
    print("Choice an operation:")
    print("[1] Create Transaction")
    optionOper = raw_input("Your Choise: ")
    print("Choice a function:")
    print("[1] Simple function")
    optionFunc = raw_input("Your Choise: ")
    data = {}
    if optionFunc == 1:
        data[sad._JSON_FUNCTION_] = sad._FUNCTION_SIMPLE_
    if optionOper == 1:
        data[sad._JSON_OPERATION_TYPE_] = sad._NEW_OPERATION_TYPE_    
        symbol = raw_input("Enter the symbol: ")
        entry = float(raw_input("Enter the entry price: "))
        lose = float(raw_input("Enter the lose price: "))
        profit = float(raw_input("Enter the profit price: "))
        quantity = float(raw_input("Enter the quantity: "))
        data[sad._JSON_ENTRY_] = entry
        data[sad._JSON_LOSE_] = lose
        data[sad._JSON_PROFIT_] = profit
        data[sad._JSON_SYMBOL_] = symbol
        data[sad._JSON_QUANTITY_] = quantity
        bm_input.sedData(data)
