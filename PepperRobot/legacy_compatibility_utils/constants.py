# API Endpoints for different resources.
LLM_ENDPOINT = "llm"       # Large Language Model operations
STT_ENDPOINT = "stt"       # Speech-to-Text operations

# LLM operations
GET_HELLO_NAME = "get_hello_name"                                   # Get greeting with user's name
GET_CHECK_NAME = "get_check_name"                                   # Verify user name
GET_CHAT_BOT_ANSWER = "get_chat_bot_answer"                         # Get chatbot response
GET_CHAT_BOT_SUMMARY = "get_chat_bot_summary"                       # Get chatbot summary
GET_CHAT_BOT_FUNCTIONALITY = "get_chat_bot_functionality"           # Get chatbot control in case of functionality request
GET_CHAT_BOT_END = "get_chat_bot_end"                               # Get chatbot conclusion
GET_YES_NO = "get_yes_no"                                           # Get yes or no given a sentence
GET_GO_AHEAD = "get_go_ahead"                                       # Verify if going ahead
GET_TUTORIAL_CLICK_INFOBOT = "get_tutorial_click_infobot"           # Get chatbot response about the click tutorial
GET_TUTORIAL_ZOOM_INFOBOT = "get_tutorial_zoom_infobot"             # Get chatbot response about the zoom tutorial
GET_TUTORIAL_MOVE_INFOBOT = "get_tutorial_move_infobot"             # Get chatbot response about the move tutorial
GET_TUTORIAL_ROTATION_INFOBOT = "get_tutorial_rotation_infobot"     # Get chatbot response about the rotation tutorial
GET_IS_ASKED_POSITION = "get_is_asked_position"                     # Get if a position is asked
GET_TASK_TYPE = "get_task_type"                                     # Get which kind of task is asked
GET_EXIT_VR = "get_exit_vr"                                         # Get the user want exit from vr session

# STT operation
GET_LISTEN = "get_listen"  # Start speech-to-text listening

# Error codes
OK = 0                  # Indicates success; everything is working correctly.
WAIT_TIMEOUT_ERROR = 1  # Error when the system times out while waiting for speech input.
UNKNOWN_VALUE_ERROR = 2 # Error when the system fails to understand or recognize the speech input.
REQUEST_ERROR = 3       # Error when there is an issue with the request to the speech recognition service.
GENERIC_ERROR = 42      # A general error code for cases that don't fall into the specific categories above.

from module_call.stt_recognition import STTRecognizer
from module_call.llm_call import LlmCaller
from models.vision_description import Florence2Call

global whisper 
global florence
global llama

whisper = STTRecognizer()
llama = LlmCaller()
florence = Florence2Call()