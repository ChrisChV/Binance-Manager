import Binance.Binance_Wrapper as BW
import Utils.sad as sad
import time
import bd
from datetime import datetime


class Order:
    def __init__(self):
        self.id = None
        self.binance_id = None
        self.price = None
        self.quantity = None
        self.order_type = None
        self.transaction_id = None
        self.state = None

    def create(self, db, price, order_type, transaction_id, state, quantity):
        self.price = price
        self.quantity = quantity
        self.order_type = order_type
        self.transaction_id = transaction_id
        self.state = state
        order = db.insert(sad._ORDER_TABLE_NAME_, {sad._TRANSACTION_ID_COL_NAME_:self.transaction_id, 
                                            sad._PRICE_COL_NAME_: self.price,
                                            sad._QUANTITY_COL_NAME_: self.quantity,
                                            sad._TYPE_COL_NAME_: self.order_type,
                                            sad._STATE_COL_NAME_: self.state}, returning=sad._ORDER_ID_COL_NAME_)
        self.id = order[sad._ORDER_ID_COL_NAME_]
        db.insert(sad._DATES_TABLE_NAME_, {sad._ORDER_ID_COL_NAME_: self.id,
                                            sad._DATE_COL_NAME_: datetime.now(),
                                            sad._STATE_COL_NAME_: self.state})
    
    def newOpenOrder(self, binance_id):
        db = bd.BD.getConn()
        self.changeState(sad._OPEN_STATE_, db=db)
        self.setBinanceId(binance_id, db=db)
        db.commit()

    def changeState(self, state, db=None, date=True):
        self.state = state
        flag = db is None
        if flag:
            db = bd.BD.getConn()
        db.update(sad._ORDER_TABLE_NAME_, {sad._STATE_COL_NAME_: self.state}, where=('order_id=%s', [str(self.id)]))
        if date:
            self.setNewDate(db=db)
        if flag:
            db.commit()
    
    def setBinanceId(self, binance_id, db=None):
        self.binance_id = binance_id
        flag = db is None
        if flag:
            db = bd.BD.getConn()
        db.update(sad._ORDER_TABLE_NAME_, {sad._BINANCE_ID_COL_NAME_: self.binance_id}, where=('order_id=%s', [str(self.id)]))
        if flag:
            db.commit()
    
    def setNewDate(self, db=None):
        flag = db is None
        if flag:
            db = bd.BD.getConn()
        db.insert(sad._DATES_TABLE_NAME_, {sad._ORDER_ID_COL_NAME_: self.id,
                                            sad._DATE_COL_NAME_: datetime.now(),
                                            sad._STATE_COL_NAME_: self.state})
        if flag:
            db.commit()
            
        

def listToOrders(listOfOrders, transaction_id):
    orders = {}
    for order in listOfOrders:
        _order = Order()
        _order.id = order[sad._ORDER_ID_COL_NAME_]
        _order.price = order[sad._PRICE_COL_NAME_]
        _order.order_type = order[sad._TYPE_COL_NAME_]
        _order.transaction_id = transaction_id
        _order.state = order[sad._STATE_COL_NAME_]
        _order.binance_id = order[sad._BINANCE_ID_COL_NAME_]
        _order.quantity = order[sad._QUANTITY_COL_NAME_]
        orders[_order.order_type] = _order
    return orders