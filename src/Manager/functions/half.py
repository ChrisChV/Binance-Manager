import model.Transaction as Transaction
import Binance.Binance_Wrapper as BW
import Utils.sad as sad
from binance.enums import *
import Logger.bm_logger as bm_logger

_ENTRY_INIT_ = 0
_WAITING_ENTRY_ = 1
_WAITING_FIRST_HALF_LOSE = 2
_WAITING_FIRST_HALF_PROFIT = 3
_WAITING_SECOND_HALF_LOSE = 4
_HALF_LOSE_ = 5
_WAITING_HALF_LOSE = 6
_LOSE_ = 7
_WAITING_LOSE = 8
_HALF_PROFIT = 9
_WAITING_PROFIT_ = 10
_PROFIT_ = 11
_WAITING_HALF_PROFIT_ = 12

def half(stop_event, disable_event, transaction_id = None, transaction = None):
    if transaction_id is None and transaction is None:
        return False
    if transaction_id != None:
        transaction = Transaction.Transaction()
        transaction.get(transaction_id)
    ans_price = None
    actual_price = BW.getPrice(transaction.symbol)
    actual_state = verifyTransaction(transaction, actual_price)
    half_lose_price = transaction.orders[sad._ENTRY_TYPE_].price - (transaction.orders[sad._ENTRY_TYPE_].price - transaction.orders[sad._LOSE_TYPE_]) / 2.0
    half_profit_price = transaction.orders[sad._ENTRY_TYPE_].price + (transaction.orders[sad._PROFIT_TYPE_].price - transaction.orders[sad._ENTRY_TYPE_]) / 2.0
    original_profit_price = transaction.orders[sad._LOSE_TYPE_].price
    original_lose_price = transaction.orders[sad._PROFIT_TYPE_].price
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
                    actual_state = _WAITING_FIRST_HALF_LOSE
                else:
                    actual_state = _WAITING_FIRST_HALF_PROFIT 
        elif actual_state == _WAITING_FIRST_HALF_LOSE:
            if actual_price <= half_lose_price:
                actual_state = _WAITING_SECOND_HALF_LOSE
            if actual_price > transaction.orders[sad._ENTRY_TYPE_].price:
                actual_state = _WAITING_FIRST_HALF_PROFIT
        elif actual_state == _WAITING_SECOND_HALF_LOSE:
            if actual_price > half_lose_price:
                actual_state = _HALF_LOSE_
            elif BW.verifyDistance(actual_price, original_lose_price) or actual_price <= original_lose_price:
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._LOSE_TYPE_], price=original_lose_price)
                actual_state = _WAITING_LOSE
        elif actual_state == _HALF_LOSE_:
            if actual_price > transaction.orders[sad._ENTRY_TYPE_].price:
                actual_state = _WAITING_FIRST_HALF_PROFIT
            elif ans_price > actual_price:
                if BW.verifyDistance(actual_price, half_lose_price) or actual_price <= half_lose_price:
                    BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._LOSE_TYPE_], price=half_lose_price)
                    actual_state = _WAITING_HALF_LOSE
        elif actual_state == _WAITING_HALF_LOSE:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._FILLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._DISABLED_STATE_)
                actual_state = _LOSE_
                break
            if not BW.verifyDistance(actual_price, transaction.orders[sad._LOSE_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._LOSE_TYPE_])
                actual_state = _HALF_LOSE_
        elif actual_state == _WAITING_LOSE:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._FILLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._DISABLED_STATE_)
                actual_state = _LOSE_
                break
            if not BW.verifyDistance(actual_price, transaction.orders[sad._LOSE_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._LOSE_TYPE_])
                actual_state = _WAITING_SECOND_HALF_LOSE
        elif actual_state == _WAITING_FIRST_HALF_PROFIT:
            if actual_price > half_profit_price:
                actual_state = _HALF_PROFIT
            elif actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                actual_state = _WAITING_FIRST_HALF_LOSE
        elif actual_price == _HALF_PROFIT:
            if BW.verifyDistance(actual_price, original_profit_price):
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_], price=original_profit_price)
                actual_state = _WAITING_PROFIT_
            elif actual_price > original_profit_price:
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_], price=actual_price)
                actual_state = _WAITING_PROFIT_
            if ans_price > actual_price:
                if BW.verifyDistance(actual_price, half_profit_price) or actual_price <= half_profit_price:
                    BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_], price=half_profit_price)
                    actual_state = _WAITING_HALF_PROFIT_
        elif actual_price == _WAITING_PROFIT_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._FILLED_STATE_)
                actual_state = _PROFIT_
                break
            if not (BW.verifyDistance(actual_price, transaction.orders[sad._PROFIT_TYPE_].price) and actual_price < transaction.orders[sad._PROFIT_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _HALF_PROFIT
        elif actual_state == _WAITING_HALF_PROFIT_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._FILLED_STATE_)
                actual_state = _PROFIT_
                break
            if not BW.verifyDistance(actual_price, transaction.orders[sad._PROFIT_TYPE_].price):
                BW.cancelOrder(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _WAITING_SECOND_HALF_LOSE
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
        

def stop(transaction):
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
    half_lose = (entry_order - lose_order) / 2.0
    half_profit = (profit_order - entry_order) / 2.0
    if entry_order.state == sad._INIT_STATE_:
        return _ENTRY_INIT_
    elif entry_order.state == sad._OPEN_STATE_:
        return _WAITING_ENTRY_
    else:
        if lose_order.state == sad._FILLED_STATE_:
            return _LOSE_
        elif profit_order.state == sad._FILLED_STATE_:
            return _PROFIT_
        elif actual_price <= half_profit:
            return _WAITING_SECOND_HALF_LOSE
        elif actual_price <= entry_order:
            return _WAITING_FIRST_HALF_LOSE
        elif actual_price > half_profit:
            return _HALF_PROFIT
        elif actual_price > entry_order:
            return _WAITING_HALF_PROFIT_
