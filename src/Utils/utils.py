import Utils.sad as sad


def getFunctionName(function_id):
    if function_id == sad._FUNCTION_SIMPLE_:
        return "Simple"
    elif function_id == sad._FUNCTION_HALF_:
        return "Half"
    elif function_id == sad._FUNCTION_INFINITE_P_:
        return "Infinite P"


def getStateName(state_id):
    if state_id == sad._INIT_STATE_:
        return "Init"
    elif state_id == sad._WAITING_STATE_:
        return "Waiting"
    elif state_id == sad._OPEN_STATE_:
        return "Open"
    elif state_id == sad._FILLED_STATE_:
        return "Filled"
    elif state_id == sad._CANCELED_STATE_:
        return "Cancelled"
    elif state_id == sad._DISABLED_STATE_:
        return "Disabled"