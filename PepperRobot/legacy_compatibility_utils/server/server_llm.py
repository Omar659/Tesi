from flask import request
from flask_restful import Resource
from module_call.llm_call import *
from constants import *
import re
import time

class Server_LLM(Resource):
    def __init__(self):
        """
        Initializes the Server_LLM class by setting up the LLM (Large Language Model) and vision services.
        """
        
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
            system_prompt = '''You are a very happy humanoid robot called Ciro, who is greeting a human in a University building. You will NEVER answer with "Nice to meet you".\n'''
            system_prompt += '''Given the next input from a human, answer with a welcome message\n'''
            system_prompt += "This is the conversation history so far:\n"
            system_prompt += f"- You: {self.pepper_question}\n"
            if self.with_image=="True":
                system_prompt += f'''\nThis is what you see:\n\t{florence.run()}.\n'''
                system_prompt += '''Based on what you see, try to add a comment if it is coherent so that it is a concluding sentence that does not expect a question.\n'''
            else:
                system_prompt += '''Based on these information, answer with a concluding sentence that does not expect a question.\n'''
            system_prompt += "You have to be very very concise (use a maximum of two sentences), or the human will get bored.\n"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())              
            return {"answer": answer, "error": False}
        
        if self.req == GET_CHECK_NAME:
            # Handles request type for extracting a name from the human's answer.
            user_prompt = f"{self.human_answer}"
            system_prompt = f'''You are a text processing engine whose only job is to find the name and the surname (if present) of the human in text.
            Given the next input, answer with only the name and the surname (if present) of the human.\n'''            
            name = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            if len(name.split(" ")) > 3:
                return {"name": "", "understood": False, "error": False}
            return {"name": name, "understood": True, "error": False}
        
        elif self.req == GET_CHAT_BOT_ANSWER:
            # Handles request type for generating a chatbot's response in a friendly manner.
            system_prompt = f"You are a very happy humanoid robot named Ciro who is talking with a human.\n"
            system_prompt += "Have a conversation with the human in a friendly manner knowing that his or her last response is the next input and answer in such a way that the human has to continue the conversation.\n"
            system_prompt += "You have to be very very concise (use a maximum of two sentences) or the human will get bored.\n"
            system_prompt += f"This is a summary of the conversation so far, to give more context, but absolutely DON'T give much weight to it unless really necessary: \"{self.summary}\".\n"
            system_prompt += f"During the conversation you can address the human by their his/her name {self.user_name} if it is necessary.\n"
            if self.with_image=="True":
                system_prompt += f'''For context, this is a description of what you see. It may be or may not be of use for you:\n\t"{florence.run()}.".\n'''
            system_prompt += '''Based on what you see and hear, try to add a comment if is it coherent so that it is a concluding sentence that does not expect a question.\n'''
            system_prompt += '''Remember to be VERY concise. The user will get bored fast, so be very concise.\n'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())            
            return {"answer": answer, "error": False}
        
        elif self.req == GET_CHAT_BOT_SUMMARY:
            # Handles request type for summarizing the conversation.
            system_prompt = "You are a summarizer. Given the next input summarize the content and answer with ONLY a detailed but concise summary.\n"
            user_prompt = f"{self.summary}.\n"
            user_prompt += f"{self.human_answer}\n"
            user_prompt += f"{self.robot_answer}."
            summary = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())         
            return {"summary": summary, "error": False}
        
        elif self.req == GET_CHAT_BOT_FUNCTIONALITY:
            # Handles request type for determining if a request is related to the robot's functionality.
            system_prompt = f'''You are a text-processing engine whose only job is to figure out whether the input text contains any kind of request about your functions and/or what you are able to do.
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.human_answer}"
            asked = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())            
            if asked.lower() == "yes":           
                return {"asked": True, "error": False}
            else:
                return {"asked": False, "error": False}
        
        elif self.req == GET_CHAT_BOT_END:
            # Handles request type for determining if the input text indicates a request to end the chat asking about the map functions.
            system_prompt = f'''You are a text-processing engine whose sole task is to determine whether the incoming text contains a request to display, navigate, or otherwise interact with a map-related feature of yours.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ne whose sole task is to determine whether the incoming text contains a request to display, navigate, or otherwise interact with a map-related feature of yours.
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.human_answer}"
            exit_ = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())            
            if exit_.lower() == "yes":           
                return {"exit": True, "error": False}
            else:
                return {"exit": False, "error": False}
        
        elif self.req == GET_YES_NO:
            # Handles request type for determining if the input answer expresses interest in a proposed activity.
            system_prompt = f'''You are a text-processing engine whose only job is to figure out whether the input answer responds with interest mainly in the activity proposed in this question: "{self.pepper_question}".
            Given the next input, answer only with yes if you deteect such requests, or no if something else is requested.\n'''
            user_prompt = f"{self.affermative_negative_answer}"
            affermative = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())            
            if affermative.lower() == "yes":           
                return {"affermative": True, "error": False}
            else:
                return {"affermative": False, "error": False}
        
        elif self.req == GET_GO_AHEAD:    
            system_prompt = f'''Analyze the user's text and classify it into:
            0 - Intention to continue the VR tutorial (interaction with virtual elements)
            1 - Explicit refusal, incoherence, or off-topic response
            2 - Expression of doubt/implicit request for clarifications regarding the current VR tutorial

            Respond "0" if:
            - There are explicit or implicit indicators of continuation (e.g., "yes", "let's go", "continue", "I'm ready")
            - The user demonstrates understanding of the VR tutorial context
            - The response is coherent and relevant to the VR interaction tutorial

            Respond "1" if:
            - There is an explicit refusal (e.g., "no", "stop")
            - The response is incoherent, off-topic, or unrelated to VR interactions
            - The text is nonsensical or completely off-context

            Respond "2" if:
            - The user expresses uncertainty or asks implicit questions specifically about the VR tutorial content
            - There are subtle expressions of doubt or requests for clarification about interacting with virtual elements

            Note: Respond with "2" ONLY if the uncertainty or doubt is related to the current VR tutorial. If the uncertainty or confusion pertains to unrelated topics, respond with "1".

            Examples:
            - "Alright, let's continue" → 0
            - "I don't want to proceed" → 1  
            - "I don't quite understand how this works" → 2
            - "This seems too complicated" → 2
            - "Maybe yes..." → 2
            - "Maybe the pasta with tomato sauce" → 1'''

            user_prompt = f"Text to analyze: '{self.human_answer}'"
            response = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())

            return {
                "ahead": response if response in ["0", "1", "2"] else "1",
                "error": False
            }

        
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
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            return {"answer": answer, "error": False}
        
        elif self.req == GET_TUTORIAL_ZOOM_INFOBOT:
            # Handles request type for assisting the user with the click-sphere tutorial.
            system_prompt = '''You are a virtual assistant guiding a user through a mixed reality tutorial.
            You must be very concise (use a maximum of two sentences) or the human will get bored. You must respond only with the action the user needs to take to get his request without ever going around it, very very concise.
            The user sees a cube in the viewer that he or she can zoom in or out by pinching with the index finger and thumb of both hands on the cube and then moving the hands while maintaining the pinching.
            When you do the pinching correctly, the cube will enlarge or shrink depending on whether you respectively move your hands away or closer while maintaining the pinching.
            Your task is to assist the user with any questions or requests regarding this tutorial.
            The only way the user can proceed in the exercise is to say explicitly or implicitly.
            they are ready to continue. If you detect such an indication, acknowledge it and prepare to move forward.'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            return {"answer": answer, "error": False}
        
        elif self.req == GET_TUTORIAL_MOVE_INFOBOT:
            # Handles request type for assisting the user with the click-sphere tutorial.
            system_prompt = '''You are a virtual assistant guiding a user through a mixed reality tutorial.
            You must be very concise (use a maximum of two sentences) or the human will get bored. You must respond only with the action the user needs to take to get his request without ever going around it, very very concise.
            The user sees a cube in the viewer that he or she can move to where he or she wants by pinching with the index finger and thumb of one and only one hand on the cube and then moving the hand while maintaining the pinch.
            When pinching is done correctly, the cube will move along with the hand holding the pinch
            Your task is to assist the user with any questions or requests regarding this tutorial.
            The only way the user can proceed in the exercise is to say explicitly or implicitly.
            they are ready to continue. If you detect such an indication, acknowledge it and prepare to move forward.'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            return {"answer": answer, "error": False}
        
        elif self.req == GET_TUTORIAL_ROTATION_INFOBOT:
            # Handles request type for assisting the user with the click-sphere tutorial.
            system_prompt = '''You are a virtual assistant guiding a user through a mixed reality tutorial.
            You must be very concise (use a maximum of two sentences) or the human will get bored. You must respond only with the action the user needs to take to get his request without ever going around it, very very concise.
            The user sees a cube in the viewer that he or she can move to where he or she wants by pinching with the index finger and thumb of one and only one hand on the cube and then moving the hand while maintaining the pinch.
            When pinching is done correctly, the cube will move along with the hand holding the pinch
            Your task is to assist the user with any questions or requests regarding this tutorial.
            The only way the user can proceed in the exercise is to say explicitly or implicitly.
            they are ready to continue. If you detect such an indication, acknowledge it and prepare to move forward.'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            return {"answer": answer, "error": False}

        elif self.req == GET_IS_ASKED_POSITION:
            system_prompt = f'''Your task is to determine whether the incoming response is a request for directions to the location of a person, or a specific room within a building. 
            The request does not need to be explicitly phrased as a question with a question mark; 
            it can be interpreted as such if it is intended to ask for the location of something or someone. 
            Additionally, a person may inquire about a location using a last name, first name, or full name, including names composed of more than two words.
            Bear in mind that the user can misspell the word, so be very flexible (e.g. "5" is "cinque", "3001" means "301", "bano" means "bagno" etc.).
            (e.g., 'Where is luigi cinque located?' where 'luigi cinque' refers to the full name).
            For the next input, check the list of places in the next line: answer with "no" if nothing matches in this list, else answer with only the matched string in the list.
            The list of places is the following:
                [ANDREA, DANIELE, ANTONIO RICCIARDI, PAOLO, PIETRO, DE MARSICO, EMANUELE, CRISTIAN RUGGIERO, RICCIARDI, AVOLA, VELARDI, MANCUSI, ALESSIO, CHRISTIAN, MAUCERI, ANXHELO DICO, SANTILLI, POSTOLACHE, TECHNICIAN ROOM, STAIRS, ANGELO DICO, MARCO MARINI, ANDREA SANTILLI, RAOUL, ANTONINI, RICCARDO, LUCA CARROZZI, SERGIO DE AGOSTINO, KONG, PAOLO ZULLANI, CRISTIAN, EMILIAN POSTOLACHE, DIDDY KONG, SILVIO, ELEVATOR, MANCINI, MOSCHELLA, ALTERI, ANTONIO FASANELLA, IRENE CANNISTRACI, LEONE, MAIORCA, BAGNI, IRENE TALLINI, CORRIDOR, BENIGNO ANSANELLI, CARMELO LOMBARDO, BAGNO, DIRETTORE, MARCO, RAOUL MARINI, BARDH, PANNONE, PRENKAJ, MICHELE, CARROZZI, PAOLO FONTANA, PIETRO CENCIARELLI, AULA CONFERENZE, CINQUE, EMAD EMAM, DIKO, LUCA PODO, MARIA, DONKEY KONG, PAOLA VELARDI, LUIGI, MAZZARA, ANTONIO NORELLI, ASCENSORE, RODOLA, SERGIO MAUCERI, ASCENSORI, PRINCIC, ANSANELLI, MARCO FUMERO, SARRICA, ESPOSITO, DANILO AVOLA, GIOVANNA, BARD, MARCO RAOUL MARINI, MARCO RAOUL, STANZA CONFERENZE, MAZZA, ANXELO DIKO, DONKEY, VALERIO VENANZI, ANGELO DIKO, CRISOSTOMI, VALENTINO, DIDDY, EMANUELE RODOLA, IRENE, MARINI, BERTI, MORETTI, EMAD, PODO, ELEVATORS, ROMEO, EMAM, PAOLA, MAGGIOLI, RUGGIERO, SERGIO, SEVERINO, DONATO, LUCA MOSCHELLA, ANXHELO, LUIGI CINQUE, NORELLI, AGOSTINO, STANZA TECNICI, EMILIAN, MECCA, FILIPPO, DANIELE PANNONE, ANXHELO DIKO, CARMELO, TECHNICIAN, VALENTINO MAIORCA, RAUL, CONFERENCE ROOM, MICHELE MANCUSI, ENRICO, BATHROOMS, RUGGERO, IRENE CANNISTRACCI, FONTANA, MAMBRO, TALLINI, ROMEO LANZINO, CHRISTIAN RUGGERO, RAUL MARINI, BAIERI, ENRICO TRONCI, TECNICO, PIERGIORGIO MORETTI, TONI MANCINI, TECNICI, BRUNO, CANNISTRACCI, TONI, MARCO RAUL MARINI, CONFERENCE, MARSICO, FEDERICO FONTANA, DONATO CRISOSTOMI, FUMERO, VISIONLAB, MAURO, DI MAMBRO, ERICA, RODOL, LUCA DEZI, DEZI, FEDERICO CAPOTONDI, ANGELO DI MAMBRO, 301, 302, ERICA ANTONINI, MARCO ESPOSITO, 314C, 314B, EMANUELE RODOL, 314A, 309, LEONARDO PICCHIAMI, TONY MANCINI, ANXELO, CENCIARELLI, LUCA, VALERIO, LANZINO, STAIR, DICO, 310, 311, 312, 313, 314, SCALA, 316, DE AGOSTINO, 317, 318, SCALE, BARDH PRENKAJ, VENANZI, 319, DANIELE BAIERI, CAPOTONDI, ANXELO DICO, TONY, CURCIO, GIORGIO, CONFERENZE, MARCO RAUL, ZULLANI, CHRISTIAN RUGGIERO, CRISTIAN RUGGERO, 322, SILVIO SEVERINO, LEONARDO, GIOVANNA LEONE, BATHROOM, DANILO, 329, MAURO SARRICA, MARIANI, PICCHIAMI, PIERGIORGIO, BARBARA, BRUNO MAZZARA, LUCA ALTERI, ALESSIO MECCA, ANDREA PRINCIC, BENIGNO, BARBARA MAZZA, 333, 334, 335, 336, 337, 338, 339, ANGELO, PEGORARO, GIORGIO MARIANI, ANTONIO, FASANELLA, LOMBARDO, CANNISTRACI, LEONARDO BERTI, 340, 341, TECHNICIANS, FILIPPO MAGGIOLI, MARIA DE MARSICO, RICCARDO CURCIO, MARCO PEGORARO, TRONCI, FEDERICO]
            If a room is mentioned along with its name, the name should take priority in the response.\n'''
            
            
            # For the next input: answer with 'no' only if you do not detect such a request. 
            # Otherwise, extrapolate from the request the specific place, or person being searched for, providing only the singular noun (e.g., 'bathrooms' should return 'bathroom').
            
            
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            if answer.upper() == "NO":           
                return {"pertinent": False, "location": "", "error": False}
            else:
                return {"pertinent": True, "location": answer.upper(), "error": False}

        elif self.req == GET_TASK_TYPE:
            system_prompt = f'''Your task is to categorize the user's intent into one of four options:  
                1. "1" if they want to reach another place (e.g., "Where is Room 5B?", "Take me to Dr. Smith," or indirect requests like "Find a lecture hall").  
                2. "2" if they wish to explore the virtual world firsthand (e.g., "Let me walk around," "I want to navigate myself," or autonomy hints).  
                3. "3" if they prefer to end the experience (e.g., "Exit now," "I'm done," or closing remarks).  
                4. "4" if the input is unrelated, ambiguous, or does not match options 1-3 (e.g., "What's the weather?", "Tell a joke," or irrelevant statements).  

            Respond **strictly** with "1," "2," "3," or "4" based on the **most logical intent**, even if phrased indirectly. Prioritize inference over literal wording. Never add explanations.'''  
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            if answer == "1":
                return {"task": "research", "error": False}
            elif answer == "2":
                return {"task": "vr", "error": False}
            elif answer == "3":
                return {"task": "end", "error": False}
            else:
                return {"task": "no_task", "error": False}

        elif self.req == GET_EXIT_VR:
            system_prompt = '''You are a text-processing engine whose sole task is to determine whether the incoming text contains a direct or indirect request to exit/end/leave the current virtual reality (VR) experience.
            Given the next input, answer **strictly** with "yes" if you detect:
                - Explicit commands: "exit VR", "stop this experience", "end the simulation" 
                - Direct requests: "I want to leave", "Take me out of here"
                - Indirect expressions: "I'm done here", "Let's go back to reality", "This isn't working"
                - Frustration cues: "I'm fed up", "I'm tired of this", "I've had enough" (in context)
                - Non-literal fatigue: "Enough for today", "No more of this"

            Respond with "no" for:
                - Ambiguous complaints: "This is boring", "It's too complicated"
                - Feature requests: "Can we try something else?"
                - Technical issues: "My head hurts", "The screen is blurry"

            Never add explanations. Judge strictly based on exit intent.'''
            user_prompt = f"{self.human_answer}"
            answer = cleanup_string(llama.get_answer(system_prompt, user_prompt).strip())
            if answer.lower() == "yes":
                return {"exit": True, "error": False}
            else:
                return {"exit": False, "error": False}

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