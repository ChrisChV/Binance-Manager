from requests.exceptions import Timeout
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import Logger.bm_logger as bm_logger
import Utils.sad as sad
import Binance.Binance_Client as BC
import logging
import math

DIFFERENCE_THRESHOLD = 0.15

def symbolExists(symbol):
    client = BC.BinanceClient.getClient()
    if client.get_symbol_info(symbol):
        return True
    return False

def getPrice(symbol):
    while True:
        try:
            client = BC.BinanceClient.getClient()    
            prices = client.get_all_tickers()
            for price in prices:
                if price['symbol'] == symbol:
                    return price["price"]
            return None
        except Timeout: 
            logging.info("Timeout Error")
            pass

def createOrder(symbol, side, order):
    client = BC.BinanceClient.getClient()
    _order = None
    try:
        _order = client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=order.quantity, price=order.price)
        order.newOpenOrder(_order['orderId'])
        message = "Transaction " + str(order.transaction_id) + "\n"
        message += getOrderType(order) +  " Order has been opened. Price: " + str(order.price) + "\n"
        bm_logger.sendNotification(message)
    except BinanceAPIException as e:
        logging.error(e)
        pass
    return _order

def createTestOrder(symbol, side, order):
    client = BC.BinanceClient.getClient()
    _order = client.create_test_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=order.quantity, price=order.price)
    return _order

def cancelOrder(symbol, order):
    client = BC.BinanceClient.getClient()
    result = client.cancel_order(symbol=symbol, orderId=order.binance_id)
    order.changeState(sad._DISABLED_STATE_)
    message = "Transaction " + str(order.transaction_id) + "\n"
    message += getOrderType(order) +  " Order has been canceled. Price: " + str(order.price) + "\n"
    bm_logger.sendNotification(message)
    return result

def getBalance(symbol):
    client = BC.BinanceClient.getClient()
    balance = client.get_asset_balance(asset=symbol)
    if balance:
        return float(balance['free'])
    return None

def getOrderState(symbol, order):
    client = BC.BinanceClient.getClient()
    try:
        _order = client.get_order(symbol=symbol, orderId=order.binance_id)
        return _order['status']
    except BinanceAPIException as e:
        logging.error(e)
        return None


def splitSymbols(symbol):
    l_symbols = sad._BINANCE_SYM_LIST_
    temp_symbl = ""
    for _symbol in l_symbols:
        flag = True
        for i in range(-1, -(len(_symbol) + 1), -1):
            if _symbol[i] != symbol[i]:
                flag = False
                break
        if flag:
            return symbol[:len(_symbol)], _symbol
                
def verifyQuantity(symbol, quantity, price):
    _symbol1, _symbol2 = splitSymbols(symbol)
    cost = quantity * price
    balance = getBalance(_symbol2)
    return balance >= cost

def getOrderType(order):
    if order.order_type == sad._ENTRY_TYPE_:
        return "Entry"
    elif order.order_type == sad._LOSE_TYPE_:
        return "Lose"
    elif order.order_type == sad._PROFIT_TYPE_:
        return "Profit"
    return ""

def percentDifference(priceA, priceB):
    return math.abs(priceA - priceB) / ((priceA + priceB) / 2.0) * 100

def verifyDistance(priceA, priceB):
    return percentDifference(priceA, priceB) <= DIFFERENCE_THRESHOLD