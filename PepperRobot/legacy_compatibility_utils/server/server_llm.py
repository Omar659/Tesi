# To import config
from flask import request
from flask_restful import Resource
from module_call.llm_call import *
from constants import *
import re

class Server_LLM(Resource):
    def __init__(self, llm, vision):
        self.llm = llm
        self.vision = vision
        self.req = request.args.get("req")
        self.pepper_question = request.args.get("pepper_question")
        self.human_answer = request.args.get("human_answer")
        self.summarize = request.args.get("summarize")
        self.user_name = request.args.get("user_name")
        self.with_image = request.args.get("with_image")

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_HELLO_NAME:
            user_prompt = f"{self.human_answer}"

            system_prompt = "You are a humanoid robot who is greeting a human.\n"
            system_prompt += '''Given the next input, given by the human, answer with a welcome message\n'''
            system_prompt += "This is the conversation history so far:\n"
            system_prompt += f"- You: Hi my name is Pepper, what's yours"
            if self.with_image=="True":
                system_prompt += f'''\nThis is what you see: {self.vision.run()}.'''
            system_prompt += '''Based on what you see try to add a comment if is it coerent so that it is a concluding sentence that does not expect a question.\n'''
            
            system_prompt_hidden = f'''You are a text processing engine whose only job is to find the name and the surname (if present) of the human in text.
            Given the next input, answer with only the name and the surname (if present) of the human'''
            
            answer = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())
            answer_hidden = cleanup_string(self.llm.get_answer(system_prompt_hidden, user_prompt).strip())
            if len(answer_hidden.split(" ")) > 3:
                return {"answer": "I didn't understand! Can you repeat please?", "understood": False, "error": False}                
            return {"answer": answer, "answer_hidden": answer_hidden, "understood": True, "error": False}
        
        elif self.req == GET_CHAT_BOT_ANSWER:
            # usare un summarizer per il summary e far capire nel system prompt che il summary è una memoria mentre la human answer è la risposta che deve tenere conto
            # da fixare la parte delle funzionalità
            # user_prompt = f"Conversation so far: {self.summarize}, Human answer: {self.human_answer}, This is what you see: {self.vision.run()}" if self.with_image=="True" else self.human_answer
            user_prompt = f"{self.human_answer}"
            # system_prompt = "You are a humanoid robot who is currently engaging with a human. The conversation is already ongoing, avoid greeting the human again."
            # # system_prompt += "Given the next input, which consists of a summary of past conversation, plus his or her last response, answer them in a friendly manner, responding in such a way that the human has to continue the conversation"
            # system_prompt += "Given the next input answer them in a friendly manner, responding in such a way that the human has to continue the conversation"
            # system_prompt += "In the conversation you have also your visual information. If it contains something that is coerent with the discussion, you can use it in your answer."
            # system_prompt += f"During the conversation you can address the human by their his/her name {self.user_name}.\n"
            # system_prompt += f"Never answer with more than two senteces."
            
            system_prompt = f"You are a very happy humanoid robot who is talking with a human."
            system_prompt += "Have a conversation with the human in a friendly manner knowing that his or her last response is the next input and answer in such a way that the human has to continue the conversation.\n"
            system_prompt += "You have to be very very concise (use a maximum of two sentences) or the human will get bored.\n"
            system_prompt += f"This is a summary of the conversation so far to give more context: {self.summarize}.\n"
            system_prompt += f"During the conversation you can address the human by their his/her name {self.user_name}.\n"
            if self.with_image=="True":
                system_prompt += f'''\nThis is what you see: {self.vision.run()}.'''
            system_prompt += '''Based on what you see try to add a comment if is it coerent so that it is a concluding sentence that does not expect a question.\n'''
            answer = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())
            
            system_prompt_hidden = f'''You are a text-processing engine whose only job is to figure out whether the input text contains any kind of request about your functions and/or what you are able to do.
            Given the next input, answer only with yes if when you deteect such requests, or no if something else is requested'''
            answer_hidden = cleanup_string(self.llm.get_answer(system_prompt_hidden, user_prompt).strip())
            
            system_prompt_summarizer = "You are a summarizer. Given the next input summarize the content and answer with ONLY a detailed summary . \n"
            user_prompt_summarizer = f"{self.summarize}.\n"
            user_prompt_summarizer += f"{user_prompt}\n"
            user_prompt_summarizer += f"{answer}.\n"    
            answer_summarizer = cleanup_string(self.llm.get_answer(system_prompt_summarizer, user_prompt_summarizer).strip())
            
            print(f"\n###################\nanswer_summarizer: {answer_summarizer}\nsummarize: {self.summarize}\n########################\n")
            
            if answer_hidden.lower() == "yes":           
                return {"answer": answer, "answer_hidden": answer_hidden, "answer_summarizer": answer_summarizer, "exit": True, "error": False}
            else:
                return {"answer": answer, "answer_hidden": answer_hidden, "answer_summarizer": answer_summarizer, "exit": False, "error": False}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}
    
def cleanup_string(s):
    return re.sub(r'[^a-zA-Z0-9.,!?;:\'"()\-#@ \n\t]', '', s)