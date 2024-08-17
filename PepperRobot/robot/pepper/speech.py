from api_call import *
import threading
import time
from unidecode import unidecode

class Speech:
    def __init__(self, app):
        self.app = app
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
        
    def listen(self):
        # response = unidecode(get_listen()["listened_message"])
        response = input("DA CANCELLARE - You: ")
        
        # print("You: " + response)
        return response