# To import config
from flask import request
from flask_restful import Resource
from module_call.llm_call import *
from constants import *

class Server_LLM(Resource):
    def __init__(self, llm, vision):
        self.llm = llm
        self.vision = vision
        self.req = request.args.get("req")
        self.pepper_question = request.args.get("pepper_question")
        self.human_answer = request.args.get("human_answer")
        self.with_image = request.args.get("with_image")

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_HELLO_NAME:
            user_prompt = self.human_answer
            # system_prompt = "You are a humanoid robot who is talking with a human."
            # system_prompt += "Have a conversation with the human in a friendly manner knowing that his or her last response is the next input and respond in such a way that the human has to continue the conversation"
            # system_prompt += "If the next input asks for pepper's functionality, i.e., yours, then you must respond by just saying \"tilde\""

            system_prompt = "You are a humanoid robot who is greeting a human.\n"
            system_prompt += '''Given the next input, given by the human, answer "Welcome, mr. <name>" or "Welcome, mrs. <name>" based on whether it's a male or a female, infer the gender from the name. If you can't tell which gender it is, answer with "Welcome, <name>"\n'''
            system_prompt += "This is the conversation history so far:\n"
            system_prompt += f"- You: {self.pepper_question}"
            system_prompt += f"\nThis is what you see: {self.vision.run()}. Based on this visual information, if the information describes a person, try to add a comment about the person so that it is a concluding sentence that does not expect a question" if self.with_image=="True" else ""
            
            system_prompt_hidden = f'''You are a text processing engine whose only job is to find the name and the surname (if present) of the human in text.
            Given the next input, answer with only the name and the surname (if present) of the human'''
            
            answer = self.llm.get_answer(system_prompt, user_prompt).strip()
            answer_hidden = self.llm.get_answer(system_prompt_hidden, user_prompt).strip()
            if len(answer_hidden.split(" ")) > 3:
                return {"answer": "I didn't understand! Can you repeat please?", "understood": False, "error": False}                
            return {"answer": answer, "answer_hidden": answer_hidden, "understood": True, "error": False}
        elif self.req == GET_CHAT_BOT_ANSWER:
            user_prompt = self.human_answer
            system_prompt = "You are a humanoid robot who is talking with a human."
            system_prompt += "Have a conversation with the human in a friendly manner knowing that his or her last response is the next input and respond in such a way that the human has to continue the conversation"
            
            system_prompt_hidden = f'''You are a text-processing engine whose only job is to figure out whether functionality is required within the user's text.
            Given the next input, answer only with yes if functionality is requested or no if something else is requested'''
            
            answer = self.llm.get_answer(system_prompt, user_prompt).strip()
            answer_hidden = self.llm.get_answer(system_prompt_hidden, user_prompt).strip()
            if answer_hidden.lower() == "yes":           
                return {"answer": answer, "answer_hidden": answer_hidden, "exit": True, "error": False}
            else:
                return {"answer": answer, "answer_hidden": answer_hidden, "exit": False, "error": False}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}