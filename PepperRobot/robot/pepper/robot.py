import sys
sys.path.append('./utils')
sys.path.append('./pepper')

import qi
from autentication_pepper import AuthenticatorFactory
from speech import Speech
from vision import Vision
import time
import threading
import random


import numpy as np

class Pepper:
    def __init__(self, ip, port=9503):
        self.ip = ip
        self.port = port
        self.app = qi.Application(sys.argv, url="tcps://" + ip + ":" + str(port))
        # self.eye_color = None
        # self.monitor_thread = None
        self.monitoring = False
        
    def login(self, user_name = "nao", password = "vision@2024"):
        logins = (user_name, password)
        factory = AuthenticatorFactory(*logins)
        self.app.session.setClientAuthenticatorFactory(factory)
        print("Logged in")
        
    def start(self):
        self.app.start()
        self.speech_module = Speech(self.app)
        self.vision_module = Vision(self.app)
        self.leds = self.app.session.service("ALLeds")        
        print("Pepper started!!")
        
    def stop(self):
        self.reset_eye_color()
        self.app.stop()
        print("Pepper stopped")
        exit(0)
        
    def execute(self, user_name = "nao", password = "vision@2024"):
        self.login(user_name=user_name, password=password)
        self.start()
        
    def set_eye_color(self, r, g, b, duration, sleep_time):
        self.monitoring = True
        time.sleep(sleep_time)
        # Convert the RGB values to a single integer color value
        color = int(r) << 16 | int(g) << 8 | int(b)
        # self.eye_color = color
        while self.monitoring:
            self.leds.fadeRGB("FaceLeds", color, duration)
            time.sleep(duration)
        color = int(255) << 16 | int(255) << 8 | int(255)
        self.leds.fadeRGB("FaceLeds", color, duration)
        # print("Eye color set to RGB({}, {}, {})".format(r, g, b))
        # if not self.monitoring:
        #     self.monitoring = True
        #     self.monitor_thread = threading.Thread(target=self._monitor_eye_color)
        #     self.monitor_thread.start()
        
    def reset_eye_color(self):
        self.monitoring = False

    # def _monitor_eye_color(self):
    #     while self.monitoring:
    #         self.leds.fadeRGB("FaceLeds", self.eye_color, 0.1)
    #         time.sleep(0.5)
    #     r = 255
    #     g = 255
    #     b = 255
    #     color = int(r) << 16 | int(g) << 8 | int(b)
    #     self.leds.fadeRGB("FaceLeds", color, 0.1)