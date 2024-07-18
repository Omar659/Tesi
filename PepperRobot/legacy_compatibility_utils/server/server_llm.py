# To import config
from flask import request
from flask_restful import Resource
from module_call.llm_call import *
from constants import *

class Server_LLM(Resource):
    def __init__(self):
        self.llm = llm_caller()
        self.req = request.args.get("req")
        self.pepper_question = request.args.get("pepper_question")
        self.human_answer = request.args.get("human_answer")

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):  
        if self.req == GET_HELLO_NAME:
            user_prompt = self.human_answer

            system_prompt = f'''You are a humanoid robot who is greeting a human. This is the conversation history so far:
            - Human: Hi!
            - You: {self.pepper_question}

            Given the next input, given by the human, answer "Welcome, mr. <name>" or "Welcome, mrs. <name>" based on whether it's a male or a female, infer the gender from the name. If you can't tell which gender it is, answer with "Welcome, <name>"'''
            
            system_prompt_hidden = f'''You are a text processing engine whose only job is to find the name and the surname (if present) of the human in text.
            Given the next input, answer with only the name and the surname (if present) of the human '''
            
            answer = self.llm.get_answer(system_prompt, user_prompt).strip()
            answer_hidden = self.llm.get_answer(system_prompt_hidden, user_prompt).strip()
            if len(answer_hidden.split(" ")) > 3:
                return {"answer": "I didn't understand! Can you repeat please?", "understood": False, "error": False}                
            return {"answer": answer, "answer_hidden": answer_hidden, "understood": True, "error": False}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}