# Va cambiato tutto con funzioni del robot di ascolto, gesture e parlato
import sys
sys.path.append('./constants')
sys.path.append('./api')
from robot_constants import *
from api_call import *
import random
from datetime import datetime
import threading
import time
import html

def handle_hello_state(robot=None):
    # metti colore occhi mentre ascolta
    pepper_question = random.choice(HELLO)
    robot.vision_module.save_image()
    robot.speech_module.say(pepper_question)
    while True:
        set_eye_color_thread = threading.Thread(target=robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
        set_eye_color_thread.start()
        human_answer = robot.speech_module.listen()
        robot.reset_eye_color()
        response_hello = get_answer_hello(pepper_question, human_answer, with_image=True)
        if response_hello["understood"]:
            break
        robot.speech_module.say(response_hello["answer"])
    
    name_db = response_hello["answer_hidden"].lower()
    if get_user_exist(name_db):
        # mi tengo in un json il nome dell'utente. Non so se e meglio una classe dedicata o usare funzioni di robot.py
        user = get_user(name_db)
        days_passed = (datetime.now() - user.last_seen).days
        pepper_welcome_back_message = response_hello["answer"].replace("Welcome", "Welcome back")
        if days_passed > 1:
            pepper_welcome_back_message += ", " + random.choice(WELCOME_BACK)
        robot.speech_module.say(pepper_welcome_back_message)
    else:
        robot.speech_module.say(response_hello["answer"])
        user = User(name_db, datetime.now())
        post_create_user(user)
    
    # robot.set_eye_color(255, 0, 0)  # Set the eye color to red
    # time.sleep(5)
    # robot.reset_eye_color()
    robot.speech_module.say(random.choice(CHAT_STARTER))
    summary = ""
    while True:
        set_eye_color_thread = threading.Thread(target=robot.set_eye_color, args=(0, 255, 0, 0.3, 4))
        set_eye_color_thread.start()
        # robot.set_eye_color(255, 0, 0, sleep_time=1)
        human_answer = robot.speech_module.listen()
        robot.reset_eye_color()
        robot.vision_module.save_image()
        response_hello = get_answer_chat_bot(human_answer, summary, user.name, with_image=True)
        
        if response_hello["exit"]:
            robot.speech_module.say(random.choice(FEATURES_DESCRIPTION))
            break
        robot.speech_module.say(response_hello["answer"])
        summary = response_hello["answer_summarizer"]
    
    robot.speech_module.say("CIAO")
