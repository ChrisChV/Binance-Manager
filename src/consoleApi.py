import Input.bm_input as bm_input
import Utils.sad as sad
import json

def initConsole():
    print("Binance Manager")
    print("Choice an operation:")
    print("[1] Create Transaction")
    print("[2] Transaction in Progress")
    print("[3] Stop Transaction")
    print("[4] Disable Transaction")
    print("[5] Get Open Tansactions" )
    optionOper = int(raw_input("Your Choise: "))
    data = {}
    if optionOper == 5:
        data[sad._JSON_OPERATION_TYPE_] = sad._GET_OPEN_OPERATION_TYPE_
        res_data = bm_input.sedData(data)
        res_data = json.loads(res_data)
        printTransactions(res_data)
    else:
        if optionOper == 1:
            data[sad._JSON_OPERATION_TYPE_] = sad._NEW_OPERATION_TYPE_    
            choiceFunction(data)
            getTransactionData(data)
        elif optionOper == 2:
            data[sad._JSON_OPERATION_TYPE_] = sad._PROGRESS_OPERATION_TYPE_
            choiceFunction(data)
            getTransactionData(data)
        elif optionOper == 3:
            data[sad._JSON_OPERATION_TYPE_] = sad._CANCEL_OPERATION_TYPE_
            transaction_id = int(raw_input("Enter the transaction ID: "))
            data[sad._JSON_TRANSACTION_ID_] = transaction_id
        elif optionOper == 4:
            data[sad._JSON_OPERATION_TYPE_] = sad._DISABLE_OPERATION_TYPE_
            transaction_id = int(raw_input("Enter the transaction ID: "))
            data[sad._JSON_TRANSACTION_ID_] = transaction_id
        msg = bm_input.sedData(data)
        print(msg)

def choiceFunction(data):
    print("Choice a function:")
    print("[1] Simple function")
    print("[2] Half function")
    print("[3] Infinite P function")
    optionFunc = int(raw_input("Your Choise: "))
    if optionFunc == 1:
        data[sad._JSON_FUNCTION_] = sad._FUNCTION_SIMPLE_
    elif optionFunc == 2:
        data[sad._JSON_FUNCTION_] = sad._FUNCTION_HALF_
    elif optionFunc == 3:
        data[sad._JSON_FUNCTION_] = sad._FUNCTION_INFINITE_P_

def getTransactionData(data):
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

def printTransactions(res_data):
    if not res_data:
        print("There isn't open transactions")
        return
    for transaction_id, data in res_data.iteritems():
        print("Transaction " + str(transaction_id))
        print("\tSymbol: " + data[sad._JSON_SYMBOL_])
        print("\tFunction: " + data[sad._JSON_FUNCTION_])
        print("\tState: " + data[sad._JSON_STATE_])
        print("\tQuantity: " + str(data[sad._JSON_QUANTITY_]))
        print("\tEntry Order:")
        print("\t\tPrice: " + data[sad._JSON_ENTRY_])
        print("\t\tState: " + data[sad._JSON_ENTRY_STATE_])
        print("\tLose Order:")
        print("\t\tPrice: " + data[sad._JSON_LOSE_])
        print("\t\tState: " + data[sad._JSON_LOSE_STATE_])
        print("\tProfit Order:")
        print("\t\tPrice: " + data[sad._JSON_PROFIT_])
        print("\t\tState: " + data[sad._JSON_PROFIT_STATE_])


initConsole()
