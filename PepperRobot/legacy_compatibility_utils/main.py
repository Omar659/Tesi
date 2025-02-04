from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from server.server_llm import Server_LLM
from server.server_stt import Server_STT
from constants import *

# Remove log print
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Use lacal host server
app = Flask(__name__)
CORS(app)

# Different type of servers
import time
api = Api(app)

# inizio = time.time()


# fine = time.time()
# print(fine-inizio)
with open("./../model_inputs/listen.txt", "w") as fp:
    fp.write("0")

api.add_resource(Server_LLM, "/" + LLM_ENDPOINT)
api.add_resource(Server_STT, "/" + STT_ENDPOINT)

if __name__ == '__main__':
    # os.system('cls')
    # os.system('clear')
    print("Starting api...")
    app.run(host="0.0.0.0", port="8080")