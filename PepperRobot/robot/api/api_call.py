from datetime import datetime
import sys

# Append custom paths to the Python system path so that the modules in these directories can be imported.
sys.path.append('./constants')
sys.path.append('./types')

from my_user import User
from state import State
from api_manager import API_manager
from constants import *
from api_constants import *

######################################
#        PepperHMD State Api         #
######################################

# Api to get the current state of the system.
def get_state():
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('get', GET_STATE, 25)
    return State(
        response["stateId"], 
        response["flagPepper"], 
        response["flagHMD"], 
        response["stateName"], 
        response["chosenPlace"], 
        response["currentUser"], 
        response["hmdOpen"], 
        response["pepperAction"]
    )

# Api to get if the HMD is open with a boolean flag.
def get_hmd_open():
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('get', GET_HMD_OPEN, 25)
    return response

# Api to check if the location is searchable
def get_is_known_location(location):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('get', GET_IS_KNOWN_LOCATION, 25, params=[["location", location]])
    return response

# Api to deactivate a pepper or HMD based on the "who" parameter.
def put_deactivate(who):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_DEACTIVATE, 25, params=[['who', who]])
    return response

# Api to activate a pepper or HMD based on the "who" parameter.
def put_activate(who):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_ACTIVATE, 25, params=[['who', who]])
    return response

# Api to set the next state based on the state name.
def put_next_state(state_name):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_NEXT_STATE, 25, params=[['stateName', state_name]])
    return response

# Api to set the current user in the state by sending a User object.
def put_set_current_user(current_user):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_SET_CURRENT_USER, 25, body=current_user.to_dict())
    return response

# Api to update the last seen date for a user.
def put_switch_pepper_action(pepper_action):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('put', PUT_SWITCH_PEPPER_ACTION, 25, params=[['pepperAction', str(pepper_action).lower()]])
    return response

# Api to post the current state in the database using a State object.
def post_set_state(state):
    API_manager_istance = API_manager(BASE_URL_HMD, STATE_ENDPOINT)
    response = API_manager_istance.call('post', POST_SET_STATE, 25, body=state.to_dict())
    return response

######################################
#        PepperHMD User Api         #
######################################

# Api to get a user object from the database based on the user's name.
def get_user(name):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('get', GET_USER, 25, params=[["name", name]])
    return User(response["name"], datetime.strptime(response["lastSeen"], "%Y-%m-%d"), response["tutorialSeen"])

# Api to check if a user exists based on the user's name.
def get_user_exist(name):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('get', GET_USER_EXIST, 25, params=[["name", name]])
    return response
    
# Api to update the last seen date for a user.
def put_update_last_seen(name):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('put', PUT_LAST_SEEN, 25, params=[["name", name]])
    return response

# Api to create a new user in the database by sending a User object.
def post_create_user(user):
    API_manager_istance = API_manager(BASE_URL_HMD, USER_ENDPOINT)
    response = API_manager_istance.call('post', POST_CREATE_USER, 25, body=user.to_dict())
    return response

####################################
#          Models LLM Api          #
####################################

# Api to get an answer from a chatbot with a "hello" interaction, with an option to include an image.
def get_answer_hello(pepper_question, human_answer, with_image=False):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_HELLO_NAME], ["pepper_question", pepper_question], ["human_answer", human_answer], ["with_image", str(with_image)]])
    return response

# Api to get a chatbot's response for a name check interaction.
def get_answer_name(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_CHECK_NAME], ["human_answer", human_answer]])
    return response

# Api to get a chatbot's response during a conversation given also the summary, username, and an image.
def get_answer_chat_bot(human_answer, summary="", user_name="", with_image=False):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_CHAT_BOT_ANSWER], ["human_answer", human_answer], ["summary", summary], ["user_name", user_name], ["with_image", str(with_image)]])
    return response

# Api to check if asking about the functionality of the robot.
def get_check_functionallity_chat_bot(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_CHAT_BOT_FUNCTIONALITY], ["human_answer", human_answer]])
    return response

# Api to check if the chatbot conversation is ending.
def get_check_exit_chat_bot(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_CHAT_BOT_END], ["human_answer", human_answer]])
    return response

# Api to summarize the chatbot conversation based on human, robot answers and the actual summary.
def get_summary_chat_bot(human_answer, summary, robot_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_CHAT_BOT_SUMMARY], ["human_answer", human_answer], ["summary", summary], ["robot_answer", robot_answer]])
    return response

# Api to get a yes/no response from the chatbot based on the human answer and the pepper question.
def get_yes_no(affermative_negative_answer, pepper_question):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_YES_NO], ["affermative_negative_answer", affermative_negative_answer], ["pepper_question", pepper_question]])
    return response

# Api to get a yes/no answer from the user's intention to go ahead in the tutorial.
def get_go_ahead(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_GO_AHEAD], ["human_answer", human_answer]])
    return response

# Api to get the assistance with the clickable spheres tutorial.
def get_answer_tutorial_click_assistant(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_TUTORIAL_CLICK_INFOBOT], ["human_answer", human_answer]])
    return response

# Api to get the assistance with the zoomable cube tutorial.
def get_answer_tutorial_zoom_assistant(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_TUTORIAL_ZOOM_INFOBOT], ["human_answer", human_answer]])
    return response

# Api to get the assistance with the movable cube tutorial.
def get_answer_tutorial_move_assistant(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_TUTORIAL_MOVE_INFOBOT], ["human_answer", human_answer]])
    return response

# Api to get the assistance with the rotable cube tutorial.
def get_answer_tutorial_rotation_assistant(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_TUTORIAL_ROTATION_INFOBOT], ["human_answer", human_answer]])
    return response

# Api to understand if a position is asked.
def get_is_asked_position(human_answer):
    API_manager_istance = API_manager(BASE_URL_LCU, LLM_ENDPOINT)
    response = API_manager_istance.call('get', "", 50, params=[["req", GET_IS_ASKED_POSITION], ["human_answer", human_answer]])
    return response

####################################
#          Models STT Api          #
####################################

# Api to trigger listening functionality for speech-to-text.
def get_listen(timeout):
    API_manager_istance = API_manager(BASE_URL_LCU, STT_ENDPOINT)
    if timeout is None:
        response = API_manager_istance.call('get', "", 50, params=[["req", GET_LISTEN]])
    else:
        response = API_manager_istance.call('get', "", 50, params=[["req", GET_LISTEN], ["timeout", timeout]])
    return response