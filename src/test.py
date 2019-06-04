from binance.client import Client
from binance.enums import *
import Binance.Binance_Client as BC
import Binance.Binance_Wrapper as BW
import model.Order as Order
import Logger.bm_logger as bm_logger
import Input.bm_input as bm_input
import model.bd as bd
import Utils.sad as sad


#db = bd.BD.getConn()
#db.update(sad._ORDER_TABLE_NAME_, {sad._STATE_COL_NAME_: 3}, where=('order_id=%s', [str(3)]))
#db.commit()

order = Order.Order()
order.binance_id = 100

status = BW.getOrderState("LINKUSDT", order)
print(status)


#symbol1, symbol2 = BW.splitSymbols()
#print(symbol1)
#print(symbol2)

#bm_input.server_socket()

#bm_logger.sendNotification("TEST")

#order = Order.Order()
#order.binance_id = 14062807

#_order = BW.getOrderState("LINKUSDT", order)
#print(_order)


#order = Order.Order()
#order.price = 1.3
#order.quantity = 46.89

#_order = BW.createOrder("LINKUSDT", SIDE_SELL, order)

#print(_order)

#if _order:
#    print("AAAAAAA")


#price = BW.getPrice("LINK/USDT")
#print(price)

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