import model.Transaction as Transaction
import Binance.Binance_Wrapper as BW
from binance.enums import *
import Utils.sad as sad

_WAITING_ENTRY_ = 1
_WAITING_LOSE_ = 2
_WAITING_PROFIT_ = 3

def simple(transaction_id = None, transaction = None):
    if transaction_id is None and transaction is None:
        return False
    if transaction_id != None:
        transaction = Transaction.Transaction()
        transaction.get(transaction_id)
    
    actual_price = None
    ##Verificar el estado de la transacción (?)
    actual_state = sad._ENTRY_TYPE_
    while True:
        actual_price = BW.getPrice(transaction.symbol)
        if actual_state == sad._ENTRY_TYPE_:
            BW.createOrder(transaction.symbol, SIDE_BUY, transaction.orders[sad._ENTRY_TYPE_])
            actual_state = _WAITING_ENTRY_
        elif actual_state == _WAITING_ENTRY_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._ENTRY_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._ENTRY_TYPE_].changeState(sad._FILLED_STATE_)
                if actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                    BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._LOSE_TYPE_])
                    actual_state = _WAITING_LOSE_
                else:
                    BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_])
                    actual_state = _WAITING_PROFIT_
        elif actual_state == _WAITING_LOSE_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._LOSE_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._FILLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._DISABLED_STATE_)
                break
            if actual_price >= transaction.orders[sad._ENTRY_TYPE_].price:
                BW.cancelOrder(transaction.orders[sad._LOSE_TYPE_])
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._PROFIT_TYPE_])
                actual_state = _WAITING_PROFIT_
        elif actual_price == _WAITING_PROFIT_:
            if BW.getOrderState(transaction.symbol, transaction.orders[sad._PROFIT_TYPE_]) == ORDER_STATUS_FILLED:
                transaction.orders[sad._LOSE_TYPE_].changeState(sad._DISABLED_STATE_)
                transaction.orders[sad._PROFIT_TYPE_].changeState(sad._FILLED_STATE_)
                break
            if actual_price <= transaction.orders[sad._ENTRY_TYPE_].price:
                BW.cancelOrder(transaction.orders[sad._PROFIT_TYPE_])
                BW.createOrder(transaction.symbol, SIDE_SELL, transaction.orders[sad._LOSE_TYPE_])
                actual_state = _WAITING_LOSE_
                

            


        
    
