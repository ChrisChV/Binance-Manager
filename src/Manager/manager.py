import Manager.functions.simple as simple
import model.Transaction as Transaction
import Logger.bm_logger as bm_logger
import time
import Utils.sad as sad
import json
import threading
import logging


transaction_threads = {}
stop_events = {}

def function_manager(function, transaction=None, transaction_id=None):
    if transaction is None and transaction_id is None:
        return False
    if function == simple.simple.__name__:
        newStopEvent = threading.Event()
        newFunction = threading.Thread(target=simple.simple, kwargs={'stop_event':newStopEvent, 'transaction':transaction, 'transaction_id':transaction_id})
        newFunction.setDaemon(True)
        newFunction.start()
        transaction_threads[transaction.id] = newFunction
        stop_events[transaction.id] = newStopEvent

def stop_manager(transaction_id):
    if transaction_id in stop_events:
        _thread = transaction_threads.pop(transaction_id)
        _stop_event = stop_events.pop(transaction_id)
        _stop_event.set()
        return True
    return False

def manager(data):
    data = json.loads(data)
    oper_type = data[sad._JSON_OPERATION_TYPE_]
    transaction = None
    transaction_id = None
    if oper_type == sad._CANCEL_OPERATION_TYPE_:
        transaction_id = data[sad._JSON_TRANSACTION_ID_]
        if stop_manager(transaction_id):
            return True, "Transaction " + str(transaction_id) + " has been canceled successfully"
        else:
            return False, "Transaction " + str(transaction_id) + " doesn't exist"
    function = data[sad._JSON_FUNCTION_]
    if oper_type == sad._NEW_OPERATION_TYPE_ or oper_type == sad._PROGRESS_OPERATION_TYPE_:
        transaction = Transaction.Transaction()
        flag, error = transaction.create(data[sad._JSON_SYMBOL_], data[sad._JSON_ENTRY_], data[sad._JSON_LOSE_], data[sad._JSON_PROFIT_], data[sad._JSON_QUANTITY_], oper_type=oper_type)
        if not flag:
            logging.error(error)
            return False, error
    function_manager(function, transaction=transaction, transaction_id=transaction_id)
    return True, "Transaction (ID:" + str(transaction.id) + ") has been created successfully"
