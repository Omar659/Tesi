import sys

# Add the './types' directory to the system path to allow importing the 'State' class.
sys.path.append('./types')

# Import the 'State' class from the 'state' module.
from state import *

# Define various state constants representing different states in the experience.
STATE_START = "start"
STATE_HELLO = "hello"
STATE_TUTORIAL0 = "ask_tutorial"
STATE_TUTORIAL1 = "user_click_tutorial"
STATE_TUTORIAL2 = "user_zoom_tutorial"
STATE_TUTORIAL3 = "user_move_tutorial"
STATE_TUTORIAL4 = "user_rotation_tutorial"
STATE_SHOW_MAP = "show_map"
STATE_CHOSE_LOCATION = "chose_location"
STATE_EXIT = "exit"

# Define flags for different components of the system, such as HMD (Head-Mounted Display) and Pepper robot.
HMD_FLAG = "HMD"
PEPPER_FLAG = "pepper"

# Define constants representing the initial start state configuration.
START_STATE_ID = "104"           # Unique identifier for the start state.
START_FLAG_PEPPER = True         # Boolean flag indicating whether Pepper is active in the start state.
START_FLAG_HMD = False           # Boolean flag indicating whether HMD is active in the start state.
START_STATE_NAME = STATE_START   # Name of the start state, using the 'STATE_START' constant.
START_CHOSEN_PLACE = None        # No place is chosen in the start state.
START_CURRENT_USER = None        # No current user is set in the start state.
START_HMD_OPEN = False           # Boolean flag indicating whether the HMD is open in the start state.
START_PEPPER_ACTION = False      # Boolean flag indicating whether Pepper is able to do an action (used to cooperate with HMD).
VR = False                       # Boolean flag indicating whether VR experience is ongoing.
CAN_TALK = False                 # Boolean flag indicating whether the user can talk in a VR experience

# Create an initial 'State' object representing the start state of the system.
INITIAL_STATE = State(
    START_STATE_ID,              # Set the state ID.
    START_FLAG_PEPPER,           # Set the Pepper flag.
    START_FLAG_HMD,              # Set the HMD flag.
    START_STATE_NAME,            # Set the state name.
    START_CHOSEN_PLACE,          # Set the chosen place.
    START_CURRENT_USER,          # Set the current user.
    START_HMD_OPEN,              # Set the HMD open flag.
    START_PEPPER_ACTION,         # Set the pepper action flag.
    VR,                          # Set the VR flag.
    CAN_TALK                     # Set the canTalk flag.
)

# Time to wait before loop request to the back-end
TIME_SLEEP_REQUEST = 0.3