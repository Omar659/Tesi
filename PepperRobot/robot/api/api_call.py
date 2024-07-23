import sys
sys.path.append('./constants')
sys.path.append('./types')
from my_user import User
from state import State
from api_manager import API_manager
from constants import *
from api_constants import *
from datetime import datetime

#############################
#        PepperHMD          #
#############################

def get_state():
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('get', GET_STATE, 25)
    return State(response["stateId"], response["flagPepper"], response["flagHMD"], response["stateName"], response["chosenPlace"])

def put_deactivate(who):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_DEACTIVATE, 25, params=[['who', who]])
    return response

def put_activate(who):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_ACTIVATE, 25, params=[['who', who]])
    return response

def put_next_state(state_name):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_NEXT_STATE, 25, params=[['stateName', state_name]])
    return response

def post_set_state(state):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('post', POST_SET_STATE, 25, body=state.to_dict())
    return response

#############################

def get_user(name):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('get', GET_USER, 25, params=[["name", name]])
    return User(response["name"], datetime.strptime(response["lastSeen"], "%Y-%m-%d"))

def get_user_exist(name):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('get', GET_USER_EXIST, 25, params=[["name", name]])
    return response

def post_create_user(user):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('post', POST_CREATE_USER, 25, body=user.to_dict())
    return response

#############################
#           LLM             #
#############################

def get_answer_hello(pepper_question, human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 25, params=[["req", GET_HELLO_NAME], ["pepper_question", pepper_question], ["human_answer", human_answer]])
    return response