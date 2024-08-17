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
    # robot.vision_module.save_image()
    robot.speech_module.say(pepper_question)
    while True:
        # set_eye_color_thread = threading.Thread(target=robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
        # set_eye_color_thread.start()
        human_answer = robot.speech_module.listen()
        # robot.reset_eye_color()
        
        response_name = get_answer_name(human_answer)
        
        if response_name["understood"]:
            break
        robot.speech_module.say(NOT_UNDERSTOOD)
        
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
        # set_eye_color_thread = threading.Thread(target=robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
        # set_eye_color_thread.start()
        # robot.vision_module.save_image()
        human_answer = robot.speech_module.listen()
        # robot.reset_eye_color()
        
        response_check = get_check_functionallity_chat_bot(human_answer)        
        if response_check["asked"]:
            pepper_question = random.choice(FEATURES_DESCRIPTION)
            robot.speech_module.say(pepper_question)
            affermative_negative_answer = robot.speech_module.listen()
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
            thread.join()
    
    return user

def handle_ask_tutorial_state(robot, current_user):
    print("START TUTORIAL STATE\n")
    
    if current_user.tutorial_seen:
        robot.speech_module.say("Ok, " + current_user.name + ". " + random.choice(ONE_OF_MY_ABILITIES))
    else:
        robot.speech_module.say("NOk, " + current_user.name + ". " + random.choice(ONE_OF_MY_ABILITIES))
    
    print("END TUTORIAL STATE")
    pass