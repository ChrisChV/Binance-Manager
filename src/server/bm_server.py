import Utils.sad as sad
import Input.bm_input as bm_input
import model.Transaction as Transaction
import Manager.manager as manager

def initServer():
    transactions = Transaction.getOpenTransactions()
    for transaction in transactions:
        manager.function_manager(transaction.function_id, transaction=transaction)
    bm_input.server_socket()