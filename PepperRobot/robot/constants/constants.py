import sys
sys.path.append('./types')
from state import *

STATE0 = "start"
STATE1 = "hello"
STATE2 = "confirm"
STATE3 = "activation"
STATE4 = "execution"
STATE5 = "chose_location"
STATE6 = "show_path"
HMD_FLAG = "HMD"
PEPPER_FLAG = "pepper"

START_STATE_ID = "104"
START_FLAG_PEPPER = False
START_FLAG_HMD = True
START_STATE_NAME = STATE0
START_CHOSEN_PLACE = None

INITIAL_STATE = State(START_STATE_ID, START_FLAG_PEPPER, START_FLAG_HMD, START_STATE_NAME, START_CHOSEN_PLACE)