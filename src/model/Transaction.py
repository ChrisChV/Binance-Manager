import Utils.sad as sad
import Binance.Binance_Wrapper as BW
import Order
import bd

class Transaction:

    def __init__(self):
        self.id = None
        self.symbol = None
        self.orders = None

    def create(self, symbol, entry, lose, profit, quantity, oper_type=sad._NEW_OPERATION_TYPE_):
        if not BW.symbolExists(symbol):
            return False, "Symbol doesn't exist"        
        actualPrice = float(BW.getPrice(symbol))
        if oper_type == sad._NEW_OPERATION_TYPE_:
            if entry > actualPrice:
                return False, "The entry price has to be less than actual price (" + str(actualPrice) + ")"
            if lose >= entry:
                return False, "The lose price has to be less than entry price"
            if profit <= entry:
                return False, "The profit price has to be grater than entry price"
            if not BW.verifyQuantity(symbol, quantity, entry):
                return False, "You don't have balance for this transaction"
        if oper_type == sad._PROGRESS_OPERATION_TYPE_:
            if lose >= actualPrice:
                return False, "The lose prices has to be less than actual price"
            if profit <= actualPrice:
                return False, "The profit price has to be grater than actual price"
        self.symbol = symbol
        db = bd.BD.getConn()
        transaction = db.insert(sad._TRANSACTION_TABLE_NAME_, {sad._SYMBOL_COL_NAME_: self.symbol}, returning='transaction_id')
        self.id = transaction['transaction_id']
        entryOrder = Order.Order()
        loseOrder = Order.Order()
        profitOrder = Order.Order()
        entryOrder.create(db, entry, sad._ENTRY_TYPE_, self.id, sad._WAITING_STATE_, quantity)
        if oper_type == sad._PROGRESS_OPERATION_TYPE_:
            entryOrder.changeState(sad._FILLED_STATE_, db=db)
        loseOrder.create(db, lose, sad._LOSE_TYPE_, self.id, sad._INIT_STATE_, quantity)
        profitOrder.create(db, profit, sad._PROFIT_TYPE_, self.id, sad._INIT_STATE_, quantity)
        db.commit()
        self.orders = {sad._ENTRY_TYPE_:entryOrder, sad._LOSE_TYPE_:loseOrder, sad._PROFIT_TYPE_:profitOrder}
        return True, None
    
    def get(self, transaction_id):
        self.id = transaction_id
        db = bd.BD.getConn()
        transaction = db.fetchone(sad._TRANSACTION_TABLE_NAME_, fields=['symbol'], where=('transaction_id=%s', str(self.id)))
        self.symbol = transaction['symbol']
        orders = db.fetchall(sad._ORDER_TABLE_NAME_, fields=['order_id', 'price', 'quantity', 'type', 'state', 'binance_id'], where=("transaction_id=%s", str(self.id)))
        self.orders = Order.listToOrders(orders, self.id)