from binance.client import Client
import key_funcs

api_key, secret_key = key_funcs.getKeys()

client = Client(api_key, secret_key)

print(client.get_symbol_info("BTCUSDT"))

print(client.get_order_book(symbol='BNBBTC'))

