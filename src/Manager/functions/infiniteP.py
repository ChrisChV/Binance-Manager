import model.Transaction as Transaction
import Binance.Binance_Wrapper as BW
import Utils.sad as sad
from binance.enums import *
import Logger.bm_logger as bm_logger

_ENTRY_INIT_ = 0
_LOSE_ = 1
_PROFIT_ = 2
_WAITING_ENTRY_ = 3
_WAITING_LOSE_DIFERENCE_ = 4
_INFINITE_P_ = 5
_WAITING_LOSE_ = 6
_WAITING_PROFIT_ = 7
_WAITING_INFINITE_P_ = 8

def infiniteP(stop_event, disable_event, transaction_id = None, transaction = None):
    if transaction_id is None and transaction is None:
        return False
    if transaction_id != None:
        transaction = Transaction.Transaction()
        transaction.get(transaction_id)
    ans_price = None
    actual_price = None
    actual_state = _ENTRY_INIT_
    infiniteP_top_price = None
    infiniteP_price = None
    profit_price = None
    while True:
        ans_price = actual_price
        actual_price = BW.getPrice(transaction.symbol)
        if stop_event.is_set():
            stop(transaction)
            return True
        if actual_state == _LOSE_ or actual_state == _PROFIT_:
            break
        if actual_state == _ENTRY_INIT_:
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
                    actual_state = _WAITING_LOSE_DIFERENCE_
                else:
                    actual_state = _INFINITE_P_
        elif actual_state == _WAITING_LOSE_DIFERENCE_:
            if actual_price > transaction.orders[sad._ENTRY_TYPE_].price:
                actual_state = _INFINITE_P_
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
                actual_state = _WAITING_LOSE_DIFERENCE_
        elif actual_state == _INFINITE_P_:
            if ans_price > actual_price:
                infiniteP_top_price = actual_price
                if BW.verifyDistance(actual_price, transaction.orders[sad._ENTRY_TYPE_].price) or actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                    infiniteP_price = transaction.orders[sad._ENTRY_TYPE_].price
                    actual_state = _WAITING_INFINITE_P_
                elif not BW.verifyDistance(actual_price, ans_price):
                    infiniteP_price = transaction.orders[sad._ENTRY_TYPE_].price + (infiniteP_top_price - transaction.orders[sad._ENTRY_TYPE_].price) / 2.0
                    actual_state = _WAITING_INFINITE_P_
        elif actual_state == _WAITING_INFINITE_P_:
            if actual_price > infiniteP_top_price:
                actual_state = _INFINITE_P_
            elif BW.verifyDistance(actual_price, infiniteP_price) or actual_price <= infiniteP_price:
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_], price=infiniteP_price)
                actual_state = _WAITING_PROFIT_
        elif actual_state == _WAITING_PROFIT_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._FILLED_STATE_)
                actual_state = _PROFIT_
                break
            if not BW.verifyDistance(actual_price, transaction.orders[sad._PROFIT_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _WAITING_INFINITE_P_


def stop(transaction, actual_price):
    message = "Transaction " + str(transaction.id) + " has been canceled\n"
    bm_logger.sendNotification(message)
    entry_state = BW.getOrderState(transaction.symbol, transaction.orders[sad._ENTRY_TYPE_])
    if entry_state == None:
        return
    if entry_state == ORDER_STATUS_NEW:
        BW.cancelOrder(transaction.symbol, transaction.orders[sad._ENTRY_TYPE_])
    else:
        if BW.getOrderState(transaction.symbol, transaction.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_NEW:
            BW.cancelOrder(transaction.symbol, transaction.orders[sad._LOSE_TYPE_])
        if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_NEW:
            BW.cancelOrder(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_])
    transaction.changeState(sad._CANCELED_STATE_)

def disable(transaction):
    message = "Transaction " + str(transaction.id) + " has been disabled\n"
    bm_logger.sendNotification(message)
    if transaction.orders[sad._ENTRY_TYPE_].state != sad._FILLED_STATE_:
        transaction.orders[sad._ENTRY_TYPE_].changeState(sad._DISABLED_STATE_)
    transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
    transaction.orders[sad._PROFIT_TYPE_].changeState(sad._DISABLED_STATE_)
    transaction.changeState(sad._CANCELED_STATE_)

def verifyTransaction(transaction, actual_price):
    entry_order = transaction.orders[sad._ENTRY_TYPE_]
    lose_order = transaction.orders[sad._LOSE_TYPE_]
    profit_order = transaction.orders[sad._PROFIT_TYPE_]
    if entry_order.state == sad._INIT_STATE_:
        return _ENTRY_INIT_
    elif entry_order.state == sad._OPEN_STATE_:
        return _WAITING_ENTRY_
    elif entry_order.state == sad._FILLED_STATE_:
        if lose_order.state == sad._FILLED_STATE_:
            return _LOSE_
        elif profit_order.state == sad._FILLED_STATE_:
            return _PROFIT_
        elif actual_price <= entry_order:
            return _WAITING_LOSE_DIFERENCE_
        else:
            return _INFINITE_P_
