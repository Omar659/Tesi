# Va cambiato tutto con funzioni del robot di ascolto, gesture e parlato
import sys
sys.path.append('./constants')
sys.path.append('./api')
from robot_constants import *
from api_call import *
import random
from datetime import datetime, timedelta
import threading
import time
import html

def handle_hello_state(robot=None):
    # metti colore occhi mentre ascolta
    pepper_question = random.choice(HELLO)
    robot.vision_module.save_image()
    print("aagsdgsdgsa")
    robot.speech_module.say(pepper_question)
    while True:
        human_answer = robot.speech_module.listen()
        
        response_name = get_answer_name(human_answer)
        
        if response_name["understood"]:
            break
        robot.speech_module.say(random.choice(NOT_UNDERSTOOD_NAME))
        
    name_db = response_name["name"].lower()
    response_hello = get_answer_hello(pepper_question, human_answer, with_image=False) # with_image da mettere a True
    if get_user_exist(name_db):
        user = get_user(name_db)
        days_passed = (datetime.now() - user.last_seen).days
        pepper_welcome_back_message = response_hello["answer"].replace("Welcome", "Welcome back")
        if days_passed > 1:
            pepper_welcome_back_message += ", " + random.choice(WELCOME_BACK)
        robot.speech_module.say(pepper_welcome_back_message)
        user.last_seen = datetime.now()
        put_update_last_seen(user.name)
    else:
        robot.speech_module.say(response_hello["answer"])
        user = User(name_db, datetime.now() + timedelta(days=1), False)
        post_create_user(user)
    
    # robot.set_eye_color(255, 0, 0)  # Set the eye color to red
    # time.sleep(5)
    # robot.reset_eye_color()
    robot.speech_module.say(random.choice(CHAT_STARTER))
    summary = ""
    while True:
        robot.vision_module.save_image()
        human_answer = robot.speech_module.listen(user.name)
        
        response_check = get_check_functionallity_chat_bot(human_answer)        
        if response_check["asked"]:
            pepper_question = random.choice(FEATURES_DESCRIPTION)
            robot.speech_module.say(pepper_question)
            affermative_negative_answer = robot.speech_module.listen(user.name)
            response_yes_no = get_yes_no(affermative_negative_answer, pepper_question)
            if response_yes_no["affermative"]:
                break
            else:
                robot.speech_module.say(random.choice(CONTINUE_DISCUSSION))
                continue
        else:
            response_exit = get_check_exit_chat_bot(human_answer)
            if response_exit["exit"]:
                robot.speech_module.say(random.choice(ONE_OF_MY_ABILITIES))                
                break
        
        response_answer = get_answer_chat_bot(human_answer, summary, user.name, with_image=False) # with_image da mettere a True
        say_thread = threading.Thread(target=robot.speech_module.say, args=(response_answer["answer"], ))
        say_thread.start()
        
        response_summary = get_summary_chat_bot(human_answer, summary, response_answer["answer"])
        summary = response_summary["summary"]
        print("Summary:" + str(summary) + "\n")
        
        if say_thread.is_alive():
            print("The thread is still running, wait for its conclusion...")
            say_thread.join()
    
    return user

def handle_ask_tutorial_state(robot, current_user):
    if not get_hmd_open():
        robot.speech_module.say(random.choice(PUT_VISOR))
        while True:
            check = get_hmd_open()
            if check:
                break
            time.sleep(TIME_SLEEP_REQUEST)
    
    if current_user.tutorial_seen:
        pepper_question = "Great, " + current_user.name.capitalize() + "! " + random.choice(REWATCH_TUTORIAL)
        robot.speech_module.say(pepper_question)
        human_answer = robot.speech_module.listen(current_user.name)
        response_yes_no = get_yes_no(human_answer, pepper_question)
        if not response_yes_no["affermative"]:
            return False
    else:
        pepper_question = "Great, " + current_user.name.capitalize() + "! " + random.choice(WATCH_TUTORIAL)
        robot.speech_module.say(pepper_question)
    return True

def handle_click_tutorial_state(robot, current_user):
    robot.speech_module.say(current_user.name.capitalize() + ", " + random.choice(TUTORIAL_CLICK_EXPLAINATION))
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the gesture...")
    robot.motion_module.click_tutorial()
    # time.sleep(7) # Da cambiare con il tempo di esecuzione della gesture di click del robot
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    robot.speech_module.say(random.choice(TUTORIAL_CLICK_YOUR_TURN))
    while True:
        human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=3)
        haead_response = get_go_ahead(human_answer)
        if haead_response["ahead"]:
            break
        else:
            response = get_answer_tutorial_click_assistant(human_answer)
            robot.speech_module.say(response["answer"])
    put_deactivate(HMD_FLAG)
    
def handle_zoom_tutorial_state(robot, current_user):
    robot.speech_module.say("Okay " + current_user.name.capitalize() + ", " + random.choice(TUTORIAL_ZOOM_EXPLAINATION))
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the gesture...")
    time.sleep(7) # Da cambiare con il tempo di esecuzione della gesture di click del robot
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    # robot.speech_module.say(random.choice(TUTORIAL_CLICK_YOUR_TURN))
    # while True:
    #     human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=1)
    #     haead_response = get_go_ahead(human_answer)
    #     if haead_response["ahead"]:
    #         break
    #     else:
    #         response = get_answer_tutorial_click_assistant(human_answer)
    #         robot.speech_module.say(response["answer"])
    # put_deactivate(HMD_FLAG)