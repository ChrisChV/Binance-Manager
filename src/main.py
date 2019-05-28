import model.Transaction as Transaction

transaction = Transaction.Transaction()
flag, error = transaction.create("LINKUSDT", 1.0, 0.5, 1.5)
print(flag)
if not flag:
    print(error)