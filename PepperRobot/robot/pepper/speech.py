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
        # self.tts = self.app.session.service("ALTextToSpeech")
        
    def say(self, text, thread=False, sleep=0, language="English"):
        # self.tts.setLanguage(language)
        print("Pepper: " + text)
        # if thread:
        #     say_thread = threading.Thread(target=self.tts.say, args=(text, ))
        #     say_thread.start()
        #     time.sleep(sleep)
        # else:
        #     self.tts.say(text)
        
    def listen(self, name="You", continuous_listening=False, timeout=None):
        while True:
            # set_eye_color_thread = threading.Thread(target=self.robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
            # set_eye_color_thread.start()
            
            # response = unidecode(get_listen(timeout)["listened_message"])
            response = input("DA CANCELLARE - {}: ".format(name.capitalize()))
            
            
            # self.robot.reset_eye_color()
            if response == "":
                if not continuous_listening:
                    self.say(random.choice(NOT_UNDERSTOOD))
                continue
            else:
                # print("{}: {}".format(name.capitalize(), response))
                break
        return response