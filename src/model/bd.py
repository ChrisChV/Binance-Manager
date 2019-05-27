import sys
import pg_simple


class BD(object):
    __instance = None
    connection_pool = None

    @classmethod
    def getPool(self):
        if BD.__instance is None:
            BD.__instance = object.__new__(self)
            self.connection_pool = pg_simple.config_pool(max_conn=250,
                        expiration=60, # idle timeout = 60 seconds
                        host='localhost',
                        port=5432,
                        database='binance_manager',
                        user='xnpiochv',
                        password='root')
        return self.connection_pool
    
    @classmethod
    def getConn(self):
        return pg_simple.PgSimple(self.getPool(), nt_cursor=False)
        


