# Base URLs for local services.
BASE_URL_HMD = "http://localhost:8081"      # HMD service
BASE_URL_LCU = "http://localhost:8080"      # LCU service
# BASE_URL = "http://192.168.210.120:8080"  # Alternate base URL

# API Endpoints for different resources.
STATE_ENDPOINT = "state"   # System state operations
USER_ENDPOINT = "user"     # User operations
LLM_ENDPOINT = "llm"       # Large Language Model operations
STT_ENDPOINT = "stt"       # Speech-to-Text operations

# State operations.
GET_STATE = "getState"                              # Retrieve current state
GET_HMD_OPEN = "getHmdOpen"                         # Check if HMD and it's app is open
PUT_DEACTIVATE = "deactivate"                       # Deactivate HMD or Pepper
PUT_ACTIVATE = "activate"                           # Activate HMD or Pepper
PUT_NEXT_STATE = "nextState"                        # Move to the next state
PUT_SET_CURRENT_USER = "setCurrentUser"             # Set current user
PUT_SWITCH_PEPPER_ACTION = "switchFlagPepperAction" # Toggle Pepper's action flag
POST_SET_STATE = "setState"                         # Set or update state

# User operations.
GET_USER = "getUser"                # Retrieve user details
GET_USER_EXIST = "getUserExist"     # Check if user exists
PUT_LAST_SEEN = "putLastSeen"       # Update user's last seen time
POST_CREATE_USER = "postCreateUser" # Create a new user

# LLM operations.
GET_HELLO_NAME = "get_hello_name"                                   # Get greeting with user's name
GET_CHECK_NAME = "get_check_name"                                   # Verify user name already exists
GET_CHAT_BOT_ANSWER = "get_chat_bot_answer"                         # Get chatbot response
GET_CHAT_BOT_SUMMARY = "get_chat_bot_summary"                       # Get chatbot summary
GET_CHAT_BOT_FUNCTIONALITY = "get_chat_bot_functionality"           # Check for functionality requests
GET_CHAT_BOT_END = "get_chat_bot_end"                               # Get chatbot conclusion
GET_YES_NO = "get_yes_no"                                           # Get yes/no answer
GET_GO_AHEAD = "get_go_ahead"                                       # Verify if going ahead
GET_TUTORIAL_CLICK_INFOBOT = "get_tutorial_click_infobot"           # Get chatbot response about the click tutorial
GET_TUTORIAL_ZOOM_INFOBOT = "get_tutorial_zoom_infobot"             # Get chatbot response about the zoom tutorial
GET_TUTORIAL_MOVE_INFOBOT = "get_tutorial_move_infobot"             # Get chatbot response about the move tutorial
GET_TUTORIAL_ROTATION_INFOBOT = "get_tutorial_rotation_infobot"     # Get chatbot response about the rotation tutorial

# STT operation
GET_LISTEN = "get_listen"  # Start speech-to-text listening
