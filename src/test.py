from binance.client import Client
import Binance.Binance_Wrapper as key_funcs

api_key, secret_key = key_funcs.getKeys()

client = Client(api_key, secret_key)

while(True):
    

    #depth = client.get_order_book(symbol='BNBBTC')
    #print (depth)

    prices = client.get_all_tickers()
    #print(prices)


    for price in prices:
        if price['symbol'] == "LINKUSDT":
            print(price)
            break



    #trades = client.get_recent_trades(symbol='LINKUSDT')
    #print(trades)

    #candles = client.get_klines(symbol='LINKUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
    #print(candles)



    #print(client.get_symbol_info("BTCUSDT"))

    #print(client.get_order_book(symbol='BNBBTC'))

