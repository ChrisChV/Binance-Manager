import Utils.sad as sad

def getKeys():
    keysFile = open(sad._KEYS_FILE_NAME_, 'r')
    api_key = keysFile.readline()
    api_key = api_key.rstrip()
    secret_key = keysFile.readline()
    secret_key = secret_key.rstrip()
    keysFile.close()
    return api_key, secret_key
