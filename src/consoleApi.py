import Input.bm_input as bm_input
import Utils.sad as sad
import json

def initConsole():
    print("Binance Manager")
    print("Choice an operation:")
    print("[1] Create Transaction")
    print("[2] Stop Transaction")
    optionOper = int(raw_input("Your Choise: "))
    data = {}
    if optionOper == 1:
        data[sad._JSON_OPERATION_TYPE_] = sad._NEW_OPERATION_TYPE_    
        print("Choice a function:")
        print("[1] Simple function")
        optionFunc = int(raw_input("Your Choise: "))
        if optionFunc == 1:
            data[sad._JSON_FUNCTION_] = sad._FUNCTION_SIMPLE_
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
    elif optionOper == 2:
        data[sad._JSON_OPERATION_TYPE_] = sad._CANCEL_OPERATION_TYPE_
        transaction_id = int(raw_input("Enter the transaction ID: "))
        data[sad._JSON_TRANSACTION_ID_] = transaction_id
    msg = bm_input.sedData(data)
    print(msg)




initConsole()