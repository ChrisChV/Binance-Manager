import Manager.functions.simple as simple
import Manager.functions.half as half
import Manager.functions.infiniteP as infiniteP
import model.Transaction as Transaction
import Logger.bm_logger as bm_logger
import time
import Utils.sad as sad
import Utils.utils as utils
import json
import threading
import logging


transaction_threads = {}
stop_events = {}
disable_events = {}

def function_manager(function, transaction=None, transaction_id=None):
    if transaction is None and transaction_id is None:
        return False
    newStopEvent = threading.Event()
    newDisableEvent = threading.Event()
    if function == sad._FUNCTION_SIMPLE_:
        newFunction = threading.Thread(target=simple.simple, kwargs={'stop_event':newStopEvent, 'disable_event':newDisableEvent, 'transaction':transaction, 'transaction_id':transaction_id})
    elif function == sad._FUNCTION_HALF_:
        newFunction = threading.Thread(target=half.half, kwargs={'stop_event':newStopEvent, 'disable_event':newDisableEvent, 'transaction': transaction, 'transaction_id':transaction_id})
    elif function == sad._FUNCTION_INFINITE_P_:
        newFunction = threading.Thread(target=infiniteP.infiniteP, kwargs={'stop_event':newStopEvent, 'disable_event':newDisableEvent, 'transaction': transaction, 'transaction_id': transaction_id})
    newFunction.setDaemon(True)
    newFunction.start()
    transaction_threads[transaction.id] = newFunction
    stop_events[transaction.id] = newStopEvent
    disable_events[transaction.id] = newDisableEvent

def stop_manager(transaction_id):
    if transaction_id in stop_events:
        _thread = transaction_threads.pop(transaction_id)
        _stop_event = stop_events.pop(transaction_id)
        _disable_event = disable_events.pop(transaction_id)
        _stop_event.set()
        return True
    return False

def disable_manager(transaction_id):
    if transaction_id in stop_events:
        _thread = transaction_threads.pop(transaction_id)
        _stop_event = stop_events.pop(transaction_id)
        _disable_event = disable_events.pop(transaction_id)
        _disable_event.set()
        return True
    return False

def manager(data):
    data = json.loads(data)
    
    if 'test' in data:
        logging.info(data['test'])
        return True, data['test']

    oper_type = data[sad._JSON_OPERATION_TYPE_]
    transaction = None
    transaction_id = None
    if oper_type == sad._CANCEL_OPERATION_TYPE_:
        transaction_id = data[sad._JSON_TRANSACTION_ID_]
        if stop_manager(transaction_id):
            return True, "Transaction " + str(transaction_id) + " has been canceled successfully"
        else:
            return False, "Transaction " + str(transaction_id) + " doesn't exist"
    elif oper_type == sad._DISABLE_OPERATION_TYPE_:
        transaction_id = data[sad._JSON_TRANSACTION_ID_]
        if disable_manager(transaction_id):
            return True, "Transaction " + str(transaction_id) + " has been disabled successfully"
        else:
            return False, "Transaction " + str(transaction_id) + " doesn't exist"
    elif oper_type == sad._GET_OPEN_OPERATION_TYPE_:
        transactions = Transaction.getOpenTransactions()
        res_data = {}
        for transaction in transactions:
            tran_data = {}
            tran_data[sad._JSON_SYMBOL_] = transaction.symbol
            tran_data[sad._JSON_FUNCTION_] = utils.getFunctionName(transaction.function_id)
            tran_data[sad._JSON_STATE_] = utils.getStateName(transaction.state)
            tran_data[sad._JSON_QUANTITY_] = transaction.orders[sad._ENTRY_TYPE_].quantity
            tran_data[sad._JSON_ENTRY_] = transaction.orders[sad._ENTRY_TYPE_].price
            tran_data[sad._JSON_ENTRY_STATE_] = utils.getStateName(transaction.orders[sad._ENTRY_TYPE_].state)
            tran_data[sad._JSON_LOSE_] = transaction.orders[sad._LOSE_TYPE_].price
            tran_data[sad._JSON_LOSE_STATE_] = utils.getStateName(transaction.orders[sad._LOSE_TYPE_].state)
            tran_data[sad._JSON_PROFIT_] = transaction.orders[sad._PROFIT_TYPE_].price
            tran_data[sad._JSON_PROFIT_STATE_] = utils.getStateName(transaction.orders[sad._PROFIT_TYPE_].state)
            res_data[transaction.id] = tran_data
        return True, json.dumps(res_data)
    function = data[sad._JSON_FUNCTION_]
    if oper_type == sad._NEW_OPERATION_TYPE_ or oper_type == sad._PROGRESS_OPERATION_TYPE_:
        state = None
        if oper_type == sad._NEW_OPERATION_TYPE_:
            state = sad._INIT_STATE_
        if oper_type == sad._PROGRESS_OPERATION_TYPE_:
            state = sad._OPEN_STATE_
        transaction = Transaction.Transaction()
        flag, error = transaction.create(data[sad._JSON_SYMBOL_], data[sad._JSON_ENTRY_], data[sad._JSON_LOSE_], data[sad._JSON_PROFIT_], data[sad._JSON_QUANTITY_], state, function, oper_type=oper_type)
        if not flag:
            logging.error(error)
            return False, error
    function_manager(function, transaction=transaction, transaction_id=transaction_id)
    return True, "Transaction (ID:" + str(transaction.id) + ") has been created successfully"
