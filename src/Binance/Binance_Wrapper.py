from binance.client import Client
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
