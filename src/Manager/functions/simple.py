import model.Transaction as Transaction
import Binance.Binance_Wrapper as BW
from binance.enums import *
import Utils.sad as sad
import Logger.bm_logger as bm_logger

_WAITING_ENTRY_ = 1
_WAITING_LOSE_ = 2
_WAITING_PROFIT_ = 3
_LOSE_ = 4
_PROFIT_ = 5
_WAITING_LOSE_DIFFERENCE = 5

def simple(stop_event, transaction_id = None, transaction = None):
    if transaction_id is None and transaction is None:
        return False
    if transaction_id != None:
        transaction = Transaction.Transaction()
        transaction.get(transaction_id)
    actual_price = BW.getPrice(transaction.symbol)
    actual_state = verifyTransaction(transaction, actual_price)
    while True:
        if stop_event.is_set():
            stop(transaction)
            return True
        if actual_state == _LOSE_ or actual_state == _PROFIT_:
            break
        actual_price = BW.getPrice(transaction.symbol)
        if actual_state == sad._ENTRY_TYPE_:
            BW.createOrder(transaction.symbol, SIDE_BUY, transaction.orders[sad._ENTRY_TYPE_])
            transaction.changeState(sad._OPEN_STATE_)
            actual_state = _WAITING_ENTRY_
        elif actual_state == _WAITING_ENTRY_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._ENTRY_TYPE_]) == ORDER_STATUS_FILLED:
                message = "Transaction " + str(transaction.id) + "\n"
                message += "Entry Order has been filled. Price: " + str(transaction.orders[sad._ENTRY_TYPE_].price) + "\n"
                bm_logger.sendNotification(message)
                transaction.orders[sad._ENTRY_TYPE_].changeState(sad._FILLED_STATE_)
                if actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                    actual_state = _WAITING_LOSE_DIFFERENCE
                else:
                    BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_])
                    actual_state = _WAITING_PROFIT_
        elif actual_state == _WAITING_LOSE_DIFFERENCE:
            if actual_price >= transaction.orders[sad._ENTRY_TYPE_].price:
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _WAITING_PROFIT_
            elif BW.verifyDistance(actual_price, transaction.orders[sad._LOSE_TYPE_].price) or actual_price <= transaction.orders[sad._LOSE_TYPE_].price:
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._LOSE_TYPE_])
                actual_state = _WAITING_LOSE_
        elif actual_state == _WAITING_LOSE_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._FILLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._DISABLED_STATE_)
                actual_state = _LOSE_
                break
            if not BW.verifyDistance(actual_price, transaction.orders[sad._LOSE_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._LOSE_TYPE_])
                actual_state = _WAITING_LOSE_DIFFERENCE
        elif actual_price == _WAITING_PROFIT_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._FILLED_STATE_)
                actual_state = _PROFIT_
                break
            if actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _WAITING_LOSE_DIFFERENCE
    transaction.changeState(sad._FILLED_STATE_)
    message = "Transaction " + str(transaction.id) + " (" + transaction.symbol + ") has finished\n"
    message += "Quantity: " + str(transaction.orders[sad._ENTRY_TYPE_].quantity) + "\n"
    message += "Entry Order Price: " + str(transaction.orders[sad._ENTRY_TYPE_].price) + "\n"
    message += "Close Order Price: "
    if actual_state == _LOSE_:
        message += str(transaction.orders[sad._LOSE_TYPE_].price) + "\n"
        lose = (transaction.orders[sad._ENTRY_TYPE_].price - transaction.orders[sad._LOSE_TYPE_]) * 100 / transaction.orders[sad._ENTRY_TYPE_].price
        message += "Lose: " + str(lose) + "\n"
    elif actual_state == _PROFIT_:
        message += str(transaction.orders[sad._PROFIT_TYPE_].price) + "\n"
        profit = (transaction.orders[sad._PROFIT_TYPE_].price - transaction.orders[sad._ENTRY_TYPE_]) * 100 / transaction.orders[sad._ENTRY_TYPE_].price
        message += "Profit: " + str(profit) + "\n"
    bm_logger.sendNotification(message)



def stop(transaccion):
    message = "Transaction " + str(transaccion.id) + " has been canceled\n"
    bm_logger.sendNotification(message)
    entry_state = BW.getOrderState(transaccion.symbol, transaccion.orders[sad._ENTRY_TYPE_])
    if entry_state == None:
        return
    if entry_state == ORDER_STATUS_NEW:
        BW.cancelOrder(transaccion.symbol, transaccion.orders[sad._ENTRY_TYPE_])
    else:
        if BW.getOrderState(transaccion.symbol, transaccion.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_NEW:
            BW.cancelOrder(transaccion.symbol, transaccion.orders[sad._LOSE_TYPE_])
        if BW.getOrderState(transaccion.symbol, transaccion.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_NEW:
            BW.cancelOrder(transaccion.symbol, transaccion.orders[sad._PROFIT_TYPE_])
    transaccion.changeState(sad._CANCELED_STATE_)


def verifyTransaction(transaction, actual_price):
    entry_order = transaction.orders[sad._ENTRY_TYPE_]
    lose_order = transaction.orders[sad._LOSE_TYPE_]
    profit_order = transaction.orders[sad._PROFIT_TYPE_]
    if entry_order.state == sad._INIT_STATE_:
        return sad._ENTRY_TYPE_
    elif entry_order.state == sad._OPEN_STATE_:
        return _WAITING_ENTRY_
    elif entry_order.state == sad._FILLED_STATE_:
        if lose_order.state == sad._FILLED_STATE_:
            return _LOSE_
        elif profit_order.state == sad._FILLED_STATE_:
            return _PROFIT_
        elif lose_order.state == sad._OPEN_STATE_:
            return _WAITING_LOSE_
        elif profit_order.state == sad._OPEN_STATE_:
            return _WAITING_PROFIT_
        elif actual_price <= entry_order.price:
            return _WAITING_LOSE_DIFFERENCE
        else:
            BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_])
            return  _WAITING_PROFIT_
