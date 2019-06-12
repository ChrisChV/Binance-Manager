import Utils.sad as sad
import Binance.Binance_Wrapper as BW
import Order
import bd

class Transaction:
    def __init__(self):
        self.id = None
        self.symbol = None
        self.orders = None
        self.state = None
        self.function_id = None

    def create(self, symbol, entry, lose, profit, quantity, state, function_id, oper_type=sad._NEW_OPERATION_TYPE_):
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
        self.state = state
        self.function_id = function_id
        db = bd.BD.getConn()
        transaction = db.insert(sad._TRANSACTION_TABLE_NAME_, {sad._SYMBOL_COL_NAME_: self.symbol,
                                                                sad._STATE_COL_NAME_: self.state,
                                                                sad._FUNCTION_COL_NAME_: self.function_id},
                                                                 returning='transaction_id')
        self.id = transaction['transaction_id']
        entryOrder = Order.Order()
        loseOrder = Order.Order()
        profitOrder = Order.Order()
        if oper_type == sad._PROGRESS_OPERATION_TYPE_:
            entryOrder.create(db, entry, sad._ENTRY_TYPE_, self.id, sad._FILLED_STATE_, quantity)
        else:
            entryOrder.create(db, entry, sad._ENTRY_TYPE_, self.id, sad._INIT_STATE_, quantity)
        loseOrder.create(db, lose, sad._LOSE_TYPE_, self.id, sad._INIT_STATE_, quantity)
        profitOrder.create(db, profit, sad._PROFIT_TYPE_, self.id, sad._INIT_STATE_, quantity)
        db.commit()
        self.orders = {sad._ENTRY_TYPE_:entryOrder, sad._LOSE_TYPE_:loseOrder, sad._PROFIT_TYPE_:profitOrder}
        return True, None
    
    def get(self, transaction_id):
        self.id = transaction_id
        db = bd.BD.getConn()
        transaction = db.fetchone(sad._TRANSACTION_TABLE_NAME_, fields=['symbol', 'state', 'function'], where=('transaction_id=%s', str(self.id)))
        self.symbol = transaction['symbol']
        self.state = transaction['state']
        self.function_id = transaction['function']
        orders = db.fetchall(sad._ORDER_TABLE_NAME_, fields=['order_id', 'price', 'quantity', 'type', 'state', 'binance_id'], where=("transaction_id=%s", str(self.id)))
        self.orders = Order.listToOrders(orders, self.id)

    def changeState(self, state, db=None):
        self.state = state
        flag = db is None
        if flag:
            db = bd.BD.getConn()
        db.update(sad._TRANSACTION_TABLE_NAME_, {sad._STATE_COL_NAME_: self.state}, where=('transaction_id=%s', [str(self.id)]))
        if flag:
            db.commit()

def getOpenTransactions():
    transactions = []
    db = bd.BD.getConn()
    transactions = db.fetchall(sad._TRANSACTION_TABLE_NAME_, fields=[
                                                                sad._TRANSACTION_ID_COL_NAME_,
                                                                sad._SYMBOL_COL_NAME_,
                                                                sad._STATE_COL_NAME_,
                                                                sad._FUNCTION_COL_NAME_],
                                                             where=("state=%s or state=%s", [str(sad._OPEN_STATE_),str(sad._INIT_STATE_)]))                                                       
    return listToTransactions(transactions)
    

def listToTransactions(transactions):
    _transactions = []
    db = bd.BD.getConn()
    for transaction in transactions:
        _newTransaction = Transaction()
        _newTransaction.id = transaction[sad._TRANSACTION_ID_COL_NAME_]
        _newTransaction.symbol = transaction[sad._SYMBOL_COL_NAME_]
        _newTransaction.state = transaction[sad._STATE_COL_NAME_]
        _newTransaction.function_id = transaction[sad._FUNCTION_COL_NAME_]
        orders = db.fetchall(sad._ORDER_TABLE_NAME_, fields=['order_id', 'price', 'quantity', 'type', 'state', 'binance_id'], where=("transaction_id=%s", [str(_newTransaction.id)]))
        _newTransaction.orders = Order.listToOrders(orders, _newTransaction.id)
        _transactions.append(_newTransaction)
    return _transactions

    
    