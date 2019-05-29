from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import Utils.sad as sad
import Binance.Binance_Client as BC
import logging


def symbolExists(symbol):
    client = BC.BinanceClient.getClient()
    if client.get_symbol_info(symbol):
        return True
    return False

def getPrice(symbol):
    client = BC.BinanceClient.getClient()
    prices = client.get_all_tickers()
    for price in prices:
        if price['symbol'] == symbol:
            return price["price"]
    return None

def createOrder(symbol, side, order):
    client = BC.BinanceClient.getClient()
    _order = None
    try:
        _order = client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=order.quantity, price=order.price)
        order.newOpenOrder(_order['orderId'])
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
    return result

def getBalance(symbol):
    client = BC.BinanceClient.getClient()
    balance = client.get_asset_balance(asset=symbol)
    if balance:
        return float(balance['free'])
    return None

def getOrderState(symbol, order):
    client = BC.BinanceClient.getClient()
    _order = client.get_order(symbol=symbol, orderId=order.binance_id)
    return _order['status']
