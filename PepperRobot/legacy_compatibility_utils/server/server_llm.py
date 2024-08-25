from flask import request
from flask_restful import Resource
from module_call.llm_call import *
from constants import *
import re
import time

class Server_LLM(Resource):
    def __init__(self, llm, vision):
        """
        Initializes the Server_LLM class by setting up the LLM (Large Language Model) and vision services.
        - 'llm': An instance of the language model service used for generating responses.
        - 'vision': An instance of the vision service used for processing images.
        """
        self.llm = llm
        self.vision = vision
        
        # Retrieve query parameters from the HTTP request.
        self.req = request.args.get("req")
        self.pepper_question = request.args.get("pepper_question")
        self.human_answer = request.args.get("human_answer")
        self.robot_answer = request.args.get("robot_answer")
        self.summary = request.args.get("summary")
        self.user_name = request.args.get("user_name")
        self.with_image = request.args.get("with_image")
        self.affermative_negative_answer = request.args.get("affermative_negative_answer")

    def post(self):
        """
        Handles POST requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "POST request failed", "error": True}

    def get(self):
        """
        Handles GET requests by processing different types of requests based on the 'req' parameter.
        """
        if self.req == GET_HELLO_NAME:
            # Handles request type for generating a greeting message.
            user_prompt = f"{self.human_answer}"
            system_prompt = '''You are a very happy humanoid robot who is greeting a human. In your response you NEVER respond with "Nice to meet you".\n'''
            system_prompt += '''Given the next input, given by the human, answer with a welcome message\n'''
            system_prompt += "This is the conversation history so far:\n"
            system_prompt += f"- You: {self.pepper_question}\n"
            if self.with_image=="True":
                system_prompt += f'''\nThis is what you see:\n\t{self.vision.run()}.\n'''
                system_prompt += '''Based on what you see try to add a comment if is it coerent so that it is a concluding sentence that does not expect a question.\n'''
            else:
                system_prompt += '''Based on this informations answer with a concluding sentence that does not expect a question.\n'''
            system_prompt += "You have to be very very concise (use a maximum of two sentences) or the human will get bored.\n"
            answer = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())              
            return {"answer": answer, "error": False}
        
        if self.req == GET_CHECK_NAME:
            # Handles request type for extracting a name from the human's answer.
            user_prompt = f"{self.human_answer}"
            system_prompt = f'''You are a text processing engine whose only job is to find the name and the surname (if present) of the human in text.
            Given the next input, answer with only the name and the surname (if present) of the human.\n'''            
            name = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())
            if len(name.split(" ")) > 3:
                return {"name": "", "understood": False, "error": False}
            return {"name": name, "understood": True, "error": False}
        
        elif self.req == GET_CHAT_BOT_ANSWER:
            # Handles request type for generating a chatbot's response in a friendly manner.
            system_prompt = f"You are a very happy humanoid robot who is talking with a human.\n"
            system_prompt += "Have a conversation with the human in a friendly manner knowing that his or her last response is the next input and answer in such a way that the human has to continue the conversation.\n"
            system_prompt += "You have to be very very concise (use a maximum of two sentences) or the human will get bored.\n"
            system_prompt += f"This is a summary of the conversation so far to give more context: {self.summary}.\n"
            system_prompt += f"During the conversation you can address the human by their his/her name {self.user_name}.\n"
            if self.with_image=="True":
                system_prompt += f'''This is what you see:\n\t{self.vision.run()}.\n'''
            system_prompt += '''Based on what you see try to add a comment if is it coerent so that it is a concluding sentence that does not expect a question.\n'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())            
            return {"answer": answer, "error": False}
        
        elif self.req == GET_CHAT_BOT_SUMMARY:
            # Handles request type for summarizing the conversation.
            system_prompt = "You are a summarizer. Given the next input summarize the content and answer with ONLY a detailed summary.\n"
            user_prompt = f"{self.summary}.\n"
            user_prompt += f"{self.human_answer}\n"
            user_prompt += f"{self.robot_answer}."
            summary = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())         
            return {"summary": summary, "error": False}
        
        elif self.req == GET_CHAT_BOT_FUNCTIONALITY:
            # Handles request type for determining if a request is related to the robot's functionality.
            system_prompt = f'''You are a text-processing engine whose only job is to figure out whether the input text contains any kind of request about your functions and/or what you are able to do.
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.human_answer}"
            asked = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())            
            if asked.lower() == "yes":           
                return {"asked": True, "error": False}
            else:
                return {"asked": False, "error": False}
        
        elif self.req == GET_CHAT_BOT_END:
            # Handles request type for determining if the input text indicates a request to end the chat asking about the map functions.
            system_prompt = f'''You are a text-processing engine whose sole task is to determine whether the incoming text contains a request to display, navigate, or otherwise interact with a map-related feature of yours.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ne whose sole task is to determine whether the incoming text contains a request to display, navigate, or otherwise interact with a map-related feature of yours.
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.human_answer}"
            exit_ = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())            
            if exit_.lower() == "yes":           
                return {"exit": True, "error": False}
            else:
                return {"exit": False, "error": False}
        
        elif self.req == GET_YES_NO:
            # Handles request type for determining if the input answer expresses interest in a proposed activity.
            system_prompt = f'''You are a text-processing engine whose only job is to figure out whether the input answer responds with interest mainly in the activity proposed in this question: "{self.pepper_question}".
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.affermative_negative_answer}"
            affermative = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())            
            if affermative.lower() == "yes":           
                return {"affermative": True, "error": False}
            else:
                return {"affermative": False, "error": False}
        
        elif self.req == GET_GO_AHEAD:
            # Handles request type for determining if the input answer expresses interest in proceeding with the tutorial.
            system_prompt = f'''You are a text processing engine whose only task is to determine whether the incoming text contains a continuation request \
            that is either direct or indirect, e.g., through completed execution exclamations or a sentence that makes it clear that the topic (of the tutorial) has been understood.
            Right now a tutorial is running and so the user may say different things but your only purpose is to detect this request.
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.human_answer}"
            ahead = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())            
            if ahead.lower() == "yes":           
                return {"ahead": True, "error": False}
            else:
                return {"ahead": False, "error": False}
        
        elif self.req == GET_TUTORIAL_CLICK_INFOBOT:
            # Handles request type for assisting the user with the click-sphere tutorial.
            system_prompt = '''You are a virtual assistant guiding a user through a mixed reality tutorial.
            You must be very concise (use a maximum of two sentences) or the human will get bored. You must respond only with the action the user needs to take to get his request without ever going around it, very very concise.
            The user sees spheres in the viewer, which they must click on using their index finger.
            When clicked correctly, the spheres will either light up or turn off.
            Your task is to assist the user with any questions or requests regarding this tutorial.
            The only way the user can proceed in the exercise is to say explicitly or implicitly.
            they are ready to continue. If you detect such an indication, acknowledge it and prepare to move forward.'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(self.llm.get_answer(system_prompt, user_prompt).strip())
            return {"answer": answer, "error": False}


        return {"message": "GET request failed", "error": True}

    def put(self):
        """
        Handles PUT requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        """
        Handles DELETE requests by processing different types of requests based on the 'req' parameter.
        """
        return {"message": "DELETE request failed", "error": True}
    
def cleanup_string(s):
    return re.sub(r'[^a-zA-Z0-9.,!?;:\'"()\-#@ \n\t]', '', s)