import logging
import ConfigParser
import Utils.sad as sad
import io

def sendNotification(message):
    configFile = open(sad._CONFIG_FILE_NAME_, 'r')
    configStream = configFile.read()
    config = ConfigParser.RawConfigParser(allow_no_value=False)
    config.readfp(io.BytesIO(configStream))
    configFile.close()
    option = config.get(sad._CONFIG_LOGGER_SECTION_, sad._CONFIG_TYPE_OPTION_)
    if option == sad._CONFIG_CONSOLE_VALUE_:
        logging.info(message)


