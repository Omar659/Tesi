import sys
sys.path.append('./constants')
sys.path.append('./types')
from state import *
from api_manager import *
from constants import *
from api_constants import *

def get_state():
    API_manager_istance = API_manager(BASE_URL, STATE_ENDPOINT)
    response = API_manager_istance.call('get', GET_STATE, 25)
    return State(response["stateId"], response["flagPepper"], response["flagHMD"], response["stateName"], response["chosenPlace"])

def put_deactivate(who):
    API_manager_istance = API_manager(BASE_URL, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_DEACTIVATE, 25, params=[['who', who]])
    return response

def put_activate(who):
    API_manager_istance = API_manager(BASE_URL, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_ACTIVATE, 25, params=[['who', who]])
    return response

def put_next_state(state_name):
    API_manager_istance = API_manager(BASE_URL, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_NEXT_STATE, 25, params=[['stateName', state_name]])
    return response

def post_set_state(body):
    API_manager_istance = API_manager(BASE_URL, STATE_ENDPOINT)
    response = API_manager_istance.call('post', POST_SET_STATE, 25, body=body.to_dict())
    return response