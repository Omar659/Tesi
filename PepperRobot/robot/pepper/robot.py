import sys
sys.path.append('./utils')
sys.path.append('./pepper')

import qi
from autentication_pepper import AuthenticatorFactory
from speech import Speech
from vision import Vision
from gesture import Gesture
import time
import threading
import random
from api_call import *

import numpy as np

class Pepper:
    def __init__(self, ip, port=9503):
        self.ip = ip
        self.port = port
        self.app = qi.Application(sys.argv, url="tcps://" + ip + ":" + str(port))
        self.monitoring = False
        
    def login(self, user_name = "nao", password = "vision@2024"):
        logins = (user_name, password)
        factory = AuthenticatorFactory(*logins)
        self.app.session.setClientAuthenticatorFactory(factory)
        print("Logged in")
        
    def start(self):
        self.app.start()
        self.speech_module = Speech(self.app, self)
        self.vision_module = Vision(self.app)
        self.leds = self.app.session.service("ALLeds")
        self.motion_module = Gesture(self.app, self)
        print("Pepper started!!")
        
    def stop(self):
        self.stop_eye_color()
        self.motion_module.stop()
        self.vision_module.stop()
        self.app.stop()
        print("Pepper stopped")
        exit(0)
        
    def execute(self, user_name = "nao", password = "vision@2024"):
        self.login(user_name=user_name, password=password)
        self.start()
        
    def set_eye_color(self, r, g, b, duration, sleep_time):
        listen_path = "\\\\wsl.localhost\Ubuntu\home\omars\\repos\Tesi\PepperRobot\model_inputs\listen.txt"
        self.monitoring = True
        while self.monitoring:
            with open(listen_path, "r") as fp:
                color_flag = fp.read()
            if color_flag == "1":
                put_set_can_talk(True)
                color = int(r) << 16 | int(g) << 8 | int(b)
            else:
                put_set_can_talk(False)
                color = int(255) << 16 | int(255) << 8 | int(255)
            self.leds.fadeRGB("FaceLeds", color, duration)
            time.sleep(duration)
        return 
        
    def stop_eye_color(self):
        self.monitoring = False