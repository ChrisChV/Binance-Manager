import model.Transaction as Transaction

transaction = Transaction.Transaction()
flag, _ = transaction.create("BTCUSDT", 100, 50, 500)
print(flag)