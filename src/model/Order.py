import Utils.sad as sad
import time

class Order:
    def __init__(self, price, order_type, transaction_id, state):
        self.id = None
        self.price = price
        self.order_type = order_type
        self.transaction_id = transaction_id
        self.state = state
    
    def create(self, db):
        order = db.insert(sad._ORDER_TABLE_NAME_, {sad._TRANSACTION_ID_COL_NAME_:self.transaction_id, 
                                            sad._PRICE_COL_NAME_: self.price,
                                            sad._TYPE_COL_NAME_: self.order_type,
                                            sad._STATE_COL_NAME_: self.state}, returning='order_id')
        self.id = order['order_id']
        db.insert(sad._DATES_TABLE_NAME_, {sad._ORDER_ID_COL_NAME_: self.id,
                                            sad._INIT_DATE_COL_NAME_: int(time.time())})
        
