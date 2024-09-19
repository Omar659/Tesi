import vision_definitions
import numpy as np
import cv2
import os

class Vision:
    def __init__(self, app):
        self.app = app
        self.vision = self.app.session.service("ALVideoDevice")
        self.start()
        
    def start(self):
        resolution = vision_definitions.k4VGA
        color_space = vision_definitions.kRGBColorSpace
        fps = 10
        self.video_client = self.vision.subscribeCamera("vision", 0, resolution, color_space, fps)
        
    def save_image(self, path="\\\\wsl.localhost\Ubuntu\home\omir97\\repos\Tesi\PepperRobot\model_inputs\\", save_name = "pepper_view.png"):
        frame = None
        while frame is None:
            frame = self.vision.getImageRemote(self.video_client)
            if frame is None:
                continue
            width = frame[0]
            height = frame[1]
            array = frame[6]
            
            image = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            cv2.imwrite(path + save_name, image_rgb)
        print("Image saved in {}".format(path + save_name))
                
    def stop(self):
        self.vision.unsubscribe(self.video_client)