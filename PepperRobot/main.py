import sys 
sys.path.append('./api')
sys.path.append('./utils')
sys.path.append('./constants')
from autentication_pepper import *
from state_flow_functions import *
import qi
import motion
import math
import time
from api_call import *
import keyboard
import time

post_set_state(INITIAL_STATE)

while True:
    state = get_state()

    # print(state)
    # print

    if state is not None and state.flag_pepper:
        if state.state_name == STATE1:
            handle_hello_state()
            put_activate(HMD_FLAG)
            put_deactivate(PEPPER_FLAG)
            put_next_state(STATE2)
        elif state.state_name == STATE6:
            break
        

# api = API_call("http://192.168.210.120:8080", "flagPepperHMD/getFlag")
# api = API_call("http://192.168.210.120:8080", "flagPepperHMD/switchFlag")





# api = API_call("http://192.168.210.120:8080", "flagPepperHMD")
# doAction = True

# while True:
    # response = api.call('get', "getFlag", 25, ['flagName', "flag"])

    # if response["flagName"] == "flag" and response["value"] and doAction:
    #     print("NELL'IF SE NON FACCIO AZIONE\t\t\tflagName: " + response["flagName"] + "; value: " + str(response["value"]) + "; doAction: " + str(doAction))
    #     if keyboard.is_pressed('d'):
    #         print("FACCIO AZIONE\t\t\tflagName: " + response["flagName"] + "; value: " + str(response["value"]) + "; doAction: " + str(doAction))
    #         doAction = False
    #         _ = api.call('put', "switchFlag", 25, ['flagName', "flag"])
                    
    # if response["flagName"] == "flag" and response["value"]:
    #     print("CHECK SULLA CHIAMATA API\t\t\tflagName: " + response["flagName"] + "; value: " + str(response["value"]) + "; doAction: " + str(doAction))




# # Connect to the robot fails at app.start() => RuntimeError: disconnected
# app = qi.Application(sys.argv, url="tcps://192.168.137.41:9503")
# logins = ("nao", "vision@2024")
# factory = AuthenticatorFactory(*logins)
# app.session.setClientAuthenticatorFactory(factory)
# app.start()
# print("started")

# tts = app.session.service("ALTextToSpeech")
# tts.say('''Hi Hitler''')

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

# app.stop()
# sys.exit(0)