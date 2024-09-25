import os
import sys 
sys.path.append('./api')
sys.path.append('./utils')
sys.path.append('./services')
sys.path.append('./constants')
sys.path.append('./pepper')

from state_flow_functions import *
from constants import *


# import qi
import math
import motion

from robot import Pepper
import time
from api_call import *


def print_start(state_name):
    s = "START " + state_name + " STATE"
    len_s = len(s)
    s = "#"*len_s + "\n" + s + "\n" + "#"*len_s + "\n"
    print(s)
    
def print_end(state_name):
    s = "END " + state_name + " STATE"
    len_s = len(s)
    s = "\n" + "#"*len_s + "\n" + s + "\n" + "#"*len_s + "\n"
    print(s)


os.system('cls')

robot = Pepper(ip="192.168.1.2", port=9503)
robot.execute()

state = get_state()
if state is None or state.state_name != STATE_START:
    post_set_state(INITIAL_STATE)
    # a = 0

# import threading
# threading.Thread(target=robot.motion_module.click_tutorial).start()

# transform = robot.motion_module.get_robot_position_orientation()
# print("Angolo di rotazione della base: {} ".format(transform["theta"]))

# robot.motion_module.rotate(0)

# transform = robot.motion_module.get_robot_position_orientation()
# print("Angolo di rotazione della base: {} ".format(transform["theta"]))

# robot.motion_module.rotate(90)

# transform = robot.motion_module.get_robot_position_orientation()
# print("Angolo di rotazione della base: {} ".format(transform["theta"]))

# robot.motion_module.rotate(-90)

# transform = robot.motion_module.get_robot_position_orientation()
# print("Angolo di rotazione della base: {} ".format(transform["theta"]))


# def move1():
#     joint_values = [-50]
#     joint_names = ["RShoulderPitch"]
#     times = [3]
#     robot.motion_module.move_joints(joint_names, joint_values, times)
    
# def move2():
#     joint_values = [-70]
#     joint_names = ["RWristYaw"]
#     times = [3]
#     robot.motion_module.move_joints(joint_names, joint_values, times)
    
# def move3():
#     joint_values = [200]
#     joint_names = ["RHand"]
#     times = [3]
#     robot.motion_module.move_joints(joint_names, joint_values, times)


robot.motion_module.move_to_zero()
# put_next_state(STATE_TUTORIAL3)
# current_user = get_user("omar")
# put_next_state(STATE_SHOW_MAP)


while True:
    time.sleep(TIME_SLEEP_REQUEST)    
    state = get_state()
    
    if state is not None and state.flag_pepper:
        if state.state_name == STATE_START:
            print_start(STATE_START)
            
            put_next_state(STATE_HELLO)
            put_activate(PEPPER_FLAG)
            put_deactivate(HMD_FLAG)
            
            print_end(STATE_START)
        
        if state.state_name == STATE_HELLO:
            print_start(STATE_HELLO)
            
            current_user = handle_hello_state(robot)
            put_set_current_user(current_user)
            put_next_state(STATE_TUTORIAL0)
            
            print_end(STATE_HELLO)
        
        if state.state_name == STATE_TUTORIAL0:
            print_start(STATE_TUTORIAL0)
            
            see_tutorial = handle_ask_tutorial_state(robot, current_user)
            if see_tutorial:
                put_next_state(STATE_TUTORIAL1)
            else:
                put_next_state(STATEX) # DA CAMBIARE
            
            print_end(STATE_TUTORIAL0)
        
        if state.state_name == STATE_TUTORIAL1:
            print_start(STATE_TUTORIAL1)
            
            handle_click_tutorial_state(robot, current_user)
            # handle_click_tutorial_state(robot, get_user("omar"))
            # time.sleep(10)
            put_next_state(STATE_TUTORIAL2)
            
            print_end(STATE_TUTORIAL1)
        
        if state.state_name == STATE_TUTORIAL2:
            print_start(STATE_TUTORIAL2)
            
            handle_zoom_tutorial_state(robot, current_user)
            # handle_zoom_tutorial_state(robot, get_user("omar"))
            # time.sleep(10)
            put_next_state(STATE_TUTORIAL3)
            
            print_end(STATE_TUTORIAL2)
        
        if state.state_name == STATE_TUTORIAL3:
            print_start(STATE_TUTORIAL3)
            
            handle_move_tutorial_state(robot, current_user)
            # handle_move_tutorial_state(robot, get_user("omar"))
            # time.sleep(10)
            put_next_state(STATE_TUTORIAL4)
            
            print_end(STATE_TUTORIAL3)
        
        if state.state_name == STATE_TUTORIAL4:
            print_start(STATE_TUTORIAL4)
            
            # handle_move_tutorial_state(robot, current_user)
            # handle_move_tutorial_state(robot, get_user("omar"))
            # time.sleep(10)
            put_next_state(STATE_SHOW_MAP)
            
            print_end(STATE_TUTORIAL4)
        
        if state.state_name == STATE_SHOW_MAP:
            print_start(STATE_SHOW_MAP)
            
            handle_show_map_state(robot, current_user)
            # handle_show_map_state(robot, state.currentUser)
            # time.sleep(3)
            time.sleep(20)
            put_next_state(STATEX)
            
            print_end(STATE_SHOW_MAP)
        
        elif state.state_name == STATEX:
            robot.motion_module.show_map_end()
            break


# robot.vision_module.save_image()
robot.stop()

# try:
#     text = recognizer.recognize_google(audio, language='en-EN')
#     print("Hai detto: " + text)
# except sr.UnknownValueError:
#     print("Google Web Speech API non ha capito l'audio")
# except sr.RequestError as e:
#     print("Impossibile richiedere i risultati da Google Web Speech API; {0}".format(e))

# try:
#     while True:
#         robot.speech_module.listen()
# except KeyboardInterrupt:
#     robot.stop()


# import qi
# from _qi import ApplicationSession
# import time
# from autentication_pepper import AuthenticatorFactory

# IP = "192.168.179.108:9503"
# PORT = 9503

# app = qi.Application(sys.argv, url="tcps://192.168.179.108:9503")
# logins = ("nao", "vision@2024")
# factory = AuthenticatorFactory(*logins)
# app.session.setClientAuthenticatorFactory(factory)
# # app.start()

# import inspect
# src = inspect.getsource(ApplicationSession)
# print(src)
# asr_service = app.session.service("ALSpeechRecognition")
# asr_service.pause(True)
# asr_service.setLanguage("English")

# # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
# vocabulary = ["yes", "no", "please"]
# asr_service.setVocabulary(vocabulary, False)

# # Start the speech recognition engine with user Test_ASR
# asr_service.subscribe("Test_ASR")
# print('Speech recognition engine started')
# # time.sleep(20)
# asr_service.unsubscribe("Test_ASR")

# app.stop()
# exit(0)

# tts = robot.app.session.service("ALTextToSpeech")

# import qi
# from autentication_pepper import AuthenticatorFactory
# # Connect to the robot fails at app.start() => RuntimeError: disconnected
# app = qi.Application(sys.argv, url="tcps://192.168.179.108:9503")
# logins = ("nao", "vision@2024")
# factory = AuthenticatorFactory(*logins)
# app.session.setClientAuthenticatorFactory(factory)
# app.start()
# print("started")

# tts = app.session.service("ALTextToSpeech")
# tts.say('''BOOOOH''')
# app.stop()
# sys.exit(0)

# motion_service = app.session.service("ALMotion")
# motion_service.wakeUp()
# # effector   = "RShoulderPitch"
# # frame      = motion.FRAME_TORSO
# # useSensorValues = False
# # currentTf = motion_service.getTransform(effector, frame, useSensorValues)
# # print(currentTf)

# isAbsolute = True
        
# # First motion
# jointNames = ["RShoulderPitch", "RWristYaw", "RHand"]
# jointValues = [math.radians(-160), math.radians(-70), math.radians(200)]
# times = [1, 1, 1]



# motion_service.angleInterpolation(jointNames, jointValues, times, isAbsolute)
# time.sleep(2)
