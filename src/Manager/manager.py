import Manager.functions.simple as simple
import model.Transaction as Transaction
import Logger.bm_logger as bm_logger
import Utils.sad as sad
import json
import threading
import logging

def function_manager(function, transaction=None, transaction_id=None):
    if transaction is None and transaction_id is None:
        return False
    if function == simple.simple.__name__:
        newFunction = threading.Thread(target=simple.simple, kwargs={'transaction':transaction, 'transaction_id':transaction_id})
        newFunction.setDaemon(True)
        newFunction.start()


def manager(data):
    data = json.loads(data)
    function = data[sad._JSON_FUNCTION_]
    oper_type = data[sad._JSON_OPERATION_TYPE_]
    transaction = None
    transaction_id = None
    if oper_type == sad._NEW_OPERATION_TYPE_:
        transaction = Transaction.Transaction()
        flag, error = transaction.create(data[sad._JSON_SYMBOL_], data[sad._JSON_ENTRY_], data[sad._JSON_LOSE_], data[sad._JSON_PROFIT_], data[sad._JSON_QUANTITY_])
        if not flag:
            logging.error(error)
            return False, error
    elif oper_type == sad._PROGRESS_OPERATION_TYPE_:
        transaction_id = data[sad._JSON_TRANSACTION_ID_]
    function_manager(function, transaction=transaction, transaction_id=transaction_id)
    return True, "Transaction (ID:" + str(transaction.id) + ") has been created successfully"

    
    
    