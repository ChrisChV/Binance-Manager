import Utils.sad as sad
import Order
import bd

class Transaction:

    def __init__(self):
        self.id = None
        self.symbol = None
        self.orders = None

    def create(self, symbol, entry, lose, profit):
        ##symbol tiene que existir
        ##entry tiene que ser menor que el precio actual
        if lose >= entry:
            return False, "The lose price has to be grater than entry price"
        if profit <= entry:
            return False, "The profit price has to be less than entry price"
        self.symbol = symbol
        db = bd.BD.getConn()
        transaction = db.insert(sad._TRANSACTION_TABLE_NAME_, {sad._SYMBOL_COL_NAME_: self.symbol}, returning='transaction_id')
        self.id = transaction['transaction_id']
        entryOrder = Order.Order(entry, sad._ENTRY_TYPE_, self.id, sad._WAITING_STATE_)
        loseOrder = Order.Order(lose, sad._LOSE_TYPE_, self.id, sad._INIT_STATE_)
        profitOrder = Order.Order(profit, sad._PROFIT_TYPE_, self.id, sad._INIT_STATE_)
        entryOrder.create(db)
        loseOrder.create(db)
        profitOrder.create(db)
        db.commit()
        return True, None
        