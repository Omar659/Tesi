import sys
sys.path.append('./utils')
sys.path.append('./pepper')

import qi
from autentication_pepper import AuthenticatorFactory
from speech import Speech
from vision import Vision


import numpy as np

class Pepper:
    def __init__(self, ip, port=9503):
        self.ip = ip
        self.port = port
        self.app = qi.Application(sys.argv, url="tcps://" + ip + ":" + str(port))
        
    def login(self, user_name = "nao", password = "vision@2024"):
        logins = (user_name, password)
        factory = AuthenticatorFactory(*logins)
        self.app.session.setClientAuthenticatorFactory(factory)
        print("Logged in")
        
    def start(self):
        self.app.start()
        self.speech_module = Speech(self.app)
        self.vision_module = Vision(self.app)
        print("Pepper started!!")
        
    def stop(self):
        self.app.stop()
        print("Pepper stopped")
        exit(0)
        
    def execute(self, user_name = "nao", password = "vision@2024"):
        self.login(user_name=user_name, password=password)
        self.start()