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
        # self.app = app
        self.robot = robot
        # self.tts = self.app.session.service("ALTextToSpeech")
        # self.animated_tts = self.app.session.service("ALAnimatedSpeech")
        self.configuration = {"bodyLanguageMode": "random"}
        
    def say(self, text, thread=False, sleep=0, language="Italian", animated=True):
        # self.tts.setLanguage(language)
        print("Pepper: " + text)
        # if thread:
        #     say_thread = threading.Thread(target=self.tts.say, args=(text, ))
        #     say_thread.start()
        #     time.sleep(sleep)
        # else:
        #     if animated:
        #         text = self._animated_say_string(text)
        #         self.animated_tts.say(text, self.configuration)
        #     else:
        #         self.tts.say(text)
        
    def listen(self, name="You", continuous_listening=False, timeout=None):
        while True:
            # set_eye_color_thread = threading.Thread(target=self.robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
            # set_eye_color_thread.start()
            
            # response = unidecode(get_listen(timeout)["listened_message"])
            response = input("DA CANCELLARE - {}: ".format(name.capitalize()))
            
            
            # self.robot.reset_eye_color()
            if response == "":
                # if not continuous_listening:
                #     self.say(random.choice(NOT_UNDERSTOOD))
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