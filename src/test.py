from binance.client import Client
from binance.enums import *
import Binance.Binance_Client as BC
import Binance.Binance_Wrapper as BW
import model.Order as Order


order = Order.Order()
order.binance_id = 14062807

_order = BW.getOrderState("LINKUSDT", order)
print(_order)


#order = Order.Order()
#order.price = 1.3
#order.quantity = 46.89

#_order = BW.createOrder("LINKUSDT", SIDE_SELL, order)

#print(_order)

#if _order:
#    print("AAAAAAA")




#14062807

#balance = BW.getBalance("LINK")
#print(balance)



#while(True):
    

    #depth = client.get_order_book(symbol='BNBBTC')
    #print (depth)

#    prices = client.get_all_tickers()
    #print(prices)


#    for price in prices:
#        if price['symbol'] == "LINKUSDT":
#            print(price)
#            break



    #trades = client.get_recent_trades(symbol='LINKUSDT')
    #print(trades)

    #candles = client.get_klines(symbol='LINKUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
    #print(candles)



    #print(client.get_symbol_info("BTCUSDT"))

    #print(client.get_order_book(symbol='BNBBTC'))

