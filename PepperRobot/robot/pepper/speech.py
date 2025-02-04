import sys
sys.path.append('./constants')
from robot_constants import *
from api_call import *
import threading
import time
from unidecode import unidecode
import random

class Speech:
    def __init__(self, app, robot):
        self.app = app
        self.robot = robot
        self.tts = self.app.session.service("ALTextToSpeech")
        self.animated_tts = self.app.session.service("ALAnimatedSpeech")
        self.aup = self.app.session.service("ALAudioPlayer")
        self.configuration = {"bodyLanguageMode": "random"}
        
    def say(self, text, thread=True, sleep=0.38, language="Italian", animated=True):
        self.tts.setLanguage(language)
        print("Pepper: " + text)
                
        say_function = self.tts.say if not animated else self.animated_tts.say
        say_args = (text, ) if not animated else (self._animated_say_string(text), self.configuration)
        
        if thread:
            say_thread = threading.Thread(target=say_function, args=say_args)
            say_thread.start()
            time.sleep(max(sleep*len(text.split()) - 4, 0))
        else:
            if animated:
                text = self._animated_say_string(text)
                self.animated_tts.say(text, self.configuration)
            else:
                self.tts.say(text)
        
    def listen(self, name="You", continuous_listening=False, timeout=None):
        while True:            
            response = unidecode(get_listen(timeout)["listened_message"])            
            if response == "":
                if not continuous_listening:
                    self.say(random.choice(NOT_UNDERSTOOD))
                continue
            else:
                print("{}: {}".format(name.capitalize(), response))
                break
        return response
    
    def _animated_say_string(self, text):
        explanation_gestures = ["explain", "show", "think", "nod"]
        words = text.split(" ")
        new_text = ""

        for word in words:
            # Scegli un gesto casuale dalla lista
            gesture = random.choice(explanation_gestures)
            # Aggiungi il gesto dopo ogni parola
            new_text += word + " \\emph=" + gesture + "\\ "
        return new_text