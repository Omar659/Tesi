from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from server.server_llm import Server_LLM
from server.server_stt import Server_STT
from constants import *
from module_call.stt_recognition import STTRecognizer
from module_call.llm_call import LlmCaller
from models.vision_description import Florence2Call

# Remove log print
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Use lacal host server
app = Flask(__name__)
CORS(app)

# Different type of servers
api = Api(app)
api.add_resource(Server_LLM, "/" + LLM_ENDPOINT, resource_class_args=(LlmCaller(), Florence2Call()))
api.add_resource(Server_STT, "/" + STT_ENDPOINT, resource_class_args=(STTRecognizer(), ))

if __name__ == '__main__':
    os.system('cls')
    # Database
    print("Starting api...")
    app.run(host="0.0.0.0", port="8080")