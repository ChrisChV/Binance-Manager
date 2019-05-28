import model.Transaction as Transaction
import Binance.Binance_Wrapper as BW
import Utils.sad as sad

def simple(transaction_id = None, transaction = None):
    if transaction_id is None and transaction is None:
        return False
    if transaction_id != None:
        transaction = Transaction.Transaction()
        transaction.get(transaction_id)
    actual_price = None
    ##Verificar el estado de la transacción (?)
    actual_state = sad._ENTRY_TYPE_
    while True:
        actual_price = BW.getPrice(transaction.symbol)
        #if actual_state == sad._ENTRY_TYPE_:


        
    
