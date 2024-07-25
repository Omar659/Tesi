# import openai
# from openai import OpenAI
# import json


# with open("./token.json", 'r', encoding='utf-8') as file:
#     data = json.load(file)

# client = openai.OpenAI(
#     api_key= data["api_key"],
#     base_url=data["base_url"],
# )

# def get_code_completion(prompt, model="codellama/CodeLlama-34b-Instruct-hf", max_tokens=512):
#     code_completion = client.chat.completions.create(
#         model=model,
#         messages=prompt,
#         temperature=0.7,
#         max_tokens=max_tokens,
#         stop=[
#             "<step>"
#         ],
#         frequency_penalty=1,
#         presence_penalty=1,
#         top_p=0.7
#     )
#     return code_completion

# user_prompt = "My name is Beatrice"

# system_prompt = '''You are a humanoid robot who is greeting a human. This is the conversation history so far:
# - Human: Hi
# - You: Hi, what's your name?

# Given the next input, given by the human, answer "Welcome, Lord <name>" or "Welcome, Lady <name>" based on whether it's a male or a female, infer the gender from the name. If you can't tell which gender it is, always answer with "Welcome, Lord <name>" as if they were a male'''

# messages = [
#       {
#             "role": "system",
#             "content": system_prompt
#       },
#       {
#             "role": "user",
#             "content": user_input,
#       }
# ]

# # get the response from the model
# response = get_code_completion(messages)

# # display the generated response
# print(response.choices[0].message.content)

# import sys
# sys.path.append('./constants')

# from llm_call import *

# lc = llm_caller()
# print(lc.get_answer(system_prompt, user_prompt))

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
    os.system('clear')
    # Database
    print("Starting api...")
    app.run(host="0.0.0.0", port="8080")