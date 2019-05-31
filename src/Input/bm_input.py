import socket
import ConfigParser
import io
import Manager.manager as manager
import Utils.sad as sad
import json


def server_socket():
    configFile = open(sad._CONFIG_FILE_NAME_, 'r')
    configStream = configFile.read()
    config = ConfigParser.RawConfigParser(allow_no_value=False)
    config.readfp(io.BytesIO(configStream))
    configFile.close()

    HOST = config.get(sad._CONFIG_INPUT_SECTION_, sad._CONFIG_HOST_SECTION_)
    PORT = 65432
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        if not data:
            break
        manager.manager(data)

def sedData(data):
    configFile = open(sad._CONFIG_FILE_NAME_, 'r')
    configStream = configFile.read()
    config = ConfigParser.RawConfigParser(allow_no_value=False)
    config.readfp(io.BytesIO(configStream))
    configFile.close()
    
    HOST = config.get(sad._CONFIG_INPUT_SECTION_, sad._CONFIG_HOST_SECTION_)
    PORT = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(json.dumps(data))
    s.close()
