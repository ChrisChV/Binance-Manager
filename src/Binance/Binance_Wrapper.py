from binance.client import Client
from binance.enums import *
import Utils.sad as sad
import Binance.Binance_Client as BC


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

def createOrder(order):
    client = BC.BinanceClient.getClient()
    _order = client.create_order()
