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
    robot.speech_module.say(pepper_question)
    while True:
        human_answer = robot.speech_module.listen(timeout=10)
        
        response_name = get_answer_name(human_answer)
        
        if response_name["understood"]:
            break
        robot.speech_module.say(random.choice(NOT_UNDERSTOOD_NAME))
        
    name_db = response_name["name"].lower()
    response_hello = get_answer_hello(pepper_question, human_answer, with_image=True) # with_image da mettere a True
    if get_user_exist(name_db):
        user = get_user(name_db)
        days_passed = (datetime.now() - user.last_seen).days
        pepper_welcome_back_message = response_hello["answer"].replace("Welcome", "Welcome back")
        if days_passed > 1:
            pepper_welcome_back_message += ", " + random.choice(WELCOME_BACK)
        robot.speech_module.say(pepper_welcome_back_message, thread = False)
        user.last_seen = datetime.now()
        put_update_last_seen(user.name)
    else:
        robot.speech_module.say(response_hello["answer"], thread = False)
        user = User(name_db, datetime.now() + timedelta(days=1), False)
        post_create_user(user)
    
    robot.speech_module.say(random.choice(CHAT_STARTER))
    summary = ""
    while True:
        inizio = time.time()
        robot.vision_module.save_image()
        print("SALVATAGGIO IMMAGINE" + str(time.time() - inizio))
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
        
        response_answer = get_answer_chat_bot(human_answer, summary, user.name, with_image=True) # with_image da mettere a True
        say_thread = threading.Thread(target=robot.speech_module.say, args=(response_answer["answer"], False, 0.38, "Italian", True))
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
        robot.speech_module.say(random.choice(PUT_VISOR), thread=False)
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
        robot.speech_module.say(pepper_question, thread=False)
    return True

def handle_click_tutorial_state(robot, current_user):
    robot.speech_module.say(current_user.name.capitalize() + ", " + random.choice(TUTORIAL_CLICK_EXPLAINATION), animated=False, thread=False)
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the click tutorial gesture...")
    robot.motion_module.click_tutorial()
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    robot.speech_module.say(random.choice(TUTORIAL_YOUR_TURN))
    while True:
        human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
        haead_response = get_go_ahead(human_answer)
        if haead_response["ahead"] == "0":
            break
        elif haead_response["ahead"] == "1":
            continue
        else:
            response = get_answer_tutorial_click_assistant(human_answer)
            robot.speech_module.say(response["answer"])
    put_deactivate(HMD_FLAG)
    robot.speech_module.say(random.choice(USING_OF_CLICK), thread=False)
    robot.speech_module.say(random.choice(TUTORIAL_NEXT_PART), thread=False)

def handle_zoom_tutorial_state(robot, current_user):
    robot.speech_module.say("Okay " + current_user.name.capitalize() + ", " + random.choice(TUTORIAL_ZOOM_EXPLAINATION), animated=False, thread=False)
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the zoom tutorial gesture...")
    robot.motion_module.zoom_tutorial()
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    robot.speech_module.say(random.choice(TUTORIAL_YOUR_TURN))
    while True:
        human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
        haead_response = get_go_ahead(human_answer)
        if haead_response["ahead"] == "0":
            break
        elif haead_response["ahead"] == "1":
            continue
        else:
            response = get_answer_tutorial_zoom_assistant(human_answer)
            robot.speech_module.say(response["answer"])
    put_deactivate(HMD_FLAG)
    robot.speech_module.say(random.choice(USING_OF_ZOOM), thread=False)
    robot.speech_module.say(random.choice(TUTORIAL_NEXT_PART), thread=False)

def handle_move_tutorial_state(robot, current_user):
    robot.speech_module.say("Okay " + current_user.name.capitalize() + ", " + random.choice(TUTORIAL_MOVE_EXPLAINATION), animated=False, thread=False)
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the move tutorial gesture...")
    robot.motion_module.move_tutorial()
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    robot.speech_module.say(random.choice(TUTORIAL_YOUR_TURN))
    while True:
        human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
        haead_response = get_go_ahead(human_answer)
        if haead_response["ahead"] == "0":
            break
        elif haead_response["ahead"] == "1":
            continue
        else:
            response = get_answer_tutorial_move_assistant(human_answer)
            robot.speech_module.say(response["answer"])
    put_deactivate(HMD_FLAG)
    robot.speech_module.say(random.choice(USING_OF_MOVE), thread=False)
    robot.speech_module.say(random.choice(TUTORIAL_NEXT_PART), thread=False)
    

def handle_rotate_tutorial_state(robot, current_user):
    robot.speech_module.say("Okay " + current_user.name.capitalize() + ", " + random.choice(TUTORIAL_ROTATION_EXPLAINATION), animated=False, thread=False)
    put_switch_pepper_action(True)
    
    print("Pepper: I'm performing the rotate tutorial gesture...")
    robot.motion_module.rotate_tutorial()
    
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    robot.speech_module.say(random.choice(TUTORIAL_YOUR_TURN))
    while True:
        human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
        haead_response = get_go_ahead(human_answer)
        if haead_response["ahead"] == "0":
            break
        elif haead_response["ahead"] == "1":
            continue
        else:
            response = get_answer_tutorial_move_assistant(human_answer)
            robot.speech_module.say(response["answer"])
    put_deactivate(HMD_FLAG)
    robot.speech_module.say(random.choice(USING_OF_ROTATE), thread=False)

def handle_show_map_state(robot, current_user):
    put_tutorial_seen(current_user.name)
    if not get_hmd_open():
        robot.speech_module.say(random.choice(PUT_VISOR), thread=False)
        while True:
            check = get_hmd_open()
            if check:
                break
            time.sleep(TIME_SLEEP_REQUEST)
            
    robot.speech_module.say(random.choice(SHOW_MAP), animated=False, thread=False)
    put_switch_pepper_action(True)
    threading.Thread(target=robot.motion_module.show_map).start()
    time.sleep(6)
    put_activate(HMD_FLAG)
    put_switch_pepper_action(False)
    
def handle_chose_location_state(robot, current_user):
    put_set_vr(False)
    put_activate(HMD_FLAG)
    robot.speech_module.say(random.choice(CHOSE_LOCATION))
    one_time = True
    while True:
        time.sleep(TIME_SLEEP_REQUEST) 
        state = get_state()
        if state.chosen_place is None:
            human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
            position_asked_response = get_is_asked_position(human_answer)
            if position_asked_response["pertinent"]:
                if get_is_known_location(position_asked_response["location"]):
                    put_set_location_tag(position_asked_response["location"])
                else:
                    robot.speech_module.say(random.choice(UNKOWNN_LOCATION))
            else:
                robot.speech_module.say(random.choice(UNKOWNN_REQUEST))
        else:
            if one_time:
                one_time = False
                robot.speech_module.say(random.choice(TASK_EXPLAINATION))
            human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
            task_response = get_task_from_sentence(human_answer)
            if task_response["task"] == "research":
                position_asked_response = get_is_asked_position(human_answer)
                if get_is_known_location(position_asked_response["location"]):
                    put_set_location_tag(position_asked_response["location"])
                    robot.speech_module.say(random.choice(UPDATE_LOCATION))
                    continue
                else:
                    robot.speech_module.say(random.choice(UNKOWNN_LOCATION))
            elif task_response["task"] == "end":
                break
            elif task_response["task"] == "vr":
                put_set_vr(True)
                robot.speech_module.say(random.choice(VR_EXPLAINATION))
                state = get_state()
                time.sleep(4)
                while state.vr:
                    human_answer = robot.speech_module.listen(name=current_user.name, continuous_listening=True, timeout=10)
                    exit_response = get_exit_from_vr(human_answer)
                    if exit_response["exit"]:
                        robot.speech_module.say(random.choice(EXIT))
                        put_set_vr(False)
                        break
                    time.sleep(TIME_SLEEP_REQUEST) 
                    state = get_state()
            else:
                robot.speech_module.say(random.choice(UNKOWNN_REQUEST))
                
    
def handle_exit_state(robot, current_user):
    robot.speech_module.say(random.choice(END_EXPERIENCE).replace("<user>", current_user.name), thread=False)