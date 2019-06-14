from binance.client import Client
import Utils.sad as sad


class BinanceClient(object):

    __instance = None
    client = None

    @classmethod
    def getClient(self):
        if BinanceClient.__instance is None or self.client is None:
            BinanceClient.__instance = object.__new__(self)
            _api_key, _secret_key = self.getKeys()
            self.client = Client(_api_key, _secret_key)
        return self.client

    @classmethod
    def getKeys(self):
        keysFile = open(sad._KEYS_FILE_PATH_, 'r')
        api_key = keysFile.readline()
        api_key = api_key.rstrip()
        secret_key = keysFile.readline()
        secret_key = secret_key.rstrip()
        keysFile.close()
        return api_key, secret_key