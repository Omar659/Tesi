# Base URLs for two local services running on different ports.
BASE_URL_HMD = "http://localhost:8081"
BASE_URL_LCU = "http://localhost:8080"
# Alternate base URL, currently commented out.
# BASE_URL = "http://192.168.210.120:8080"

# API Endpoints for different resources.
STATE_ENDPOINT = "state"   # System state operations
USER_ENDPOINT = "user"     # User operations
LLM_ENDPOINT = "llm"       # Large Language Model operations
STT_ENDPOINT = "stt"       # Speech-to-Text operations

# State operations
GET_STATE = "getState"                  # Retrieve current state
GET_HMD_OPEN = "getHmdOpen"             # Retrieve whether HMD is active
PUT_DEACTIVATE = "deactivate"           # Deactivate HMD or Pepper
PUT_ACTIVATE = "activate"               # Activate HMD or Pepper
PUT_NEXT_STATE = "nextState"            # Move to a next state
PUT_SET_CURRENT_USER = "setCurrentUser" # Set the current user of the session in the state
POST_SET_STATE = "setState"             # Set or update the state

# User operations
GET_USER = "getUser"                # Retrieve user details
GET_USER_EXIST = "getUserExist"     # Check if user exists
PUT_LAST_SEEN = "putLastSeen"       # Update the last seen of a user
POST_CREATE_USER = "postCreateUser" # Create new user

# LLM operations
GET_HELLO_NAME = "get_hello_name"                           # Get greeting with user's name
GET_CHECK_NAME = "get_check_name"                           # Verify user name
GET_CHAT_BOT_ANSWER = "get_chat_bot_answer"                 # Get chatbot response
GET_CHAT_BOT_SUMMARY = "get_chat_bot_summary"               # Get chatbot summary
GET_CHAT_BOT_FUNCTIONALITY = "get_chat_bot_functionality"   # Get chatbot control in case of functionality request
GET_CHAT_BOT_END = "get_chat_bot_end"                       # Get chatbot conclusion
GET_YES_NO = "get_yes_no"                                   # Get yes or no given a sentence

# STT operation
GET_LISTEN = "get_listen"  # Start speech-to-text listening
