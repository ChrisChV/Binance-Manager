from decimal import *

_DF_ = "/"

_BINANCE_MODULE_DIR_NAME_ = "Binance"
_KEYS_FILE_NAME_ = ".keys"
_KEYS_FILE_PATH_ = _BINANCE_MODULE_DIR_NAME_ + _DF_ + _KEYS_FILE_NAME_

_CONFIG_FILE_NAME_ = "bm.conf"

_ENTRY_TYPE_ = 0
_LOSE_TYPE_ = 1
_PROFIT_TYPE_ = 2

_INIT_STATE_ = 0
_WAITING_STATE_ = 1
_OPEN_STATE_ = 2
_FILLED_STATE_ = 3
_CANCELED_STATE_ = 4
_DISABLED_STATE_ = 5

_FUNCTION_SIMPLE_ = 0
_FUNCTION_HALF_ = 1
_FUNCTION_INFINITE_P_ = 2

PRICE_DECIMALS = Decimal(10) ** -8
QUANTITY_DECIMALS = Decimal(10) ** -5

_BINANCE_SYM_LIST_ = ["BNB", 'BTC', 'ETH', 'XRP', 'USDT', 'PAX', 'TUSD', 'USDC', 'USDS']

_TRANSACTION_TABLE_NAME_ = "Transaction"
_SYMBOL_COL_NAME_ = "symbol"

_ORDER_TABLE_NAME_ = "Binance_Order"
_TRANSACTION_ID_COL_NAME_ = "transaction_id"
_PRICE_COL_NAME_ = "price"
_QUANTITY_COL_NAME_ = "quantity"
_TYPE_COL_NAME_ = "type"
_STATE_COL_NAME_ = "state"
_BINANCE_ID_COL_NAME_ = "binance_id"

_DATES_TABLE_NAME_ = "Dates"
_ORDER_ID_COL_NAME_ = "order_id"
_DATE_COL_NAME_ = "date"

_FUNCTION_COL_NAME_ = "function"


_CONFIG_LOGGER_SECTION_ = "Logger"
_CONFIG_TYPE_OPTION_ = "type"
_CONFIG_CONSOLE_VALUE_ = "console"
_CONFIG_TELEGRAM_VALUE_ = "telegram"
_CONFIG_TELEGRAM_TOKEN_OPTION_ = "token"
_CONFIG_TELEGRAM_CHATID_OPTION_ = "chatId"
_CONFIG_INPUT_SECTION_ = "Input"
_CONFIG_HOST_SECTION_ = "host"


_JSON_FUNCTION_ = "function"
_JSON_OPERATION_TYPE_ = "oper_type"
_JSON_SYMBOL_ = "symbol"
_JSON_ENTRY_ = "entry"
_JSON_LOSE_ = "lose"
_JSON_PROFIT_ = "profit"
_JSON_ENTRY_STATE_ = "entry_state"
_JSON_LOSE_STATE_ = "lose_state"
_JSON_PROFIT_STATE_ = "profit_state"
_JSON_QUANTITY_ = "quantity"
_JSON_TRANSACTION_ID_ = "tran_id"
_JSON_STATE_ = "state"
_PING_OPERATION_TYPE_ = "ping"
_NEW_OPERATION_TYPE_ = "new"
_PROGRESS_OPERATION_TYPE_ = "progress"
_CANCEL_OPERATION_TYPE_ = "cancel"
_DISABLE_OPERATION_TYPE_ = "disable"
_GET_OPEN_OPERATION_TYPE_ = "open"
