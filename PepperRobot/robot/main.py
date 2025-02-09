import os
import sys 
sys.path.append('./api')
sys.path.append('./utils')
sys.path.append('./services')
sys.path.append('./constants')
sys.path.append('./pepper')

from state_flow_functions import *
from constants import *

import math
import motion
import threading
import json
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
    
def collect_data(user_name, task1_time, task2_time, task3_time, task4_time, task_4_num_time, filename):
    # Se il file esiste, carica il contenuto, altrimenti crea un dizionario vuoto
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {}
        
    # Se la chiave non esiste, la aggiungo come dizionario vuoto
    if user_name not in data:
        data[user_name] = {
            "task1_time": task1_time,
            "task2_time": task2_time,
            "task3_time": task3_time,
            "task4_time": task4_time,
            "task_4_num_time": task_4_num_time
        }
        
    # Salvo il file aggiornato
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    # Print task time
    print("USER " + user_name + " times:")
    print("\tTask 1: " + str(task1_time))
    print("\tTask 2: " + str(task2_time))
    print("\tTask 3: " + str(task3_time))
    print("\tTask 4: " + str(task4_time) + " per " + str(task_4_num_time) + " times")

os.system('cls')

robot = Pepper(ip="192.168.102.108", port=9503)
robot.execute()

set_eye_color_thread = threading.Thread(target=robot.set_eye_color, args=(0, 255, 0, 0.1, 0))
set_eye_color_thread.start()

state = get_state()
if state is None or state.state_name != STATE_START:
    post_set_state(INITIAL_STATE)

robot.motion_module.move_to_zero()
# current_user = get_user("omar") # DA TOGLIERE
# put_next_state(STATE_SHOW_MAP) # DA TOGLIERE

while True:
    time.sleep(TIME_SLEEP_REQUEST)    
    state = get_state()
    
    if state is not None and state.flag_pepper:
        if state.state_name == STATE_START:
            print_start(STATE_START)
            start_time = time.time()
            put_next_state(STATE_HELLO)
            put_activate(PEPPER_FLAG)
            put_deactivate(HMD_FLAG)
            
            print_end(STATE_START)
        
        if state.state_name == STATE_HELLO:
            print_start(STATE_HELLO)
            
            current_user = handle_hello_state(robot)
            put_set_current_user(current_user)
            put_next_state(STATE_TUTORIAL0)
            task1_end_time = time.time()
            task1_time = task1_end_time - start_time
            
            print_end(STATE_HELLO)
        
        if state.state_name == STATE_TUTORIAL0:
            print_start(STATE_TUTORIAL0)
            
            see_tutorial = handle_ask_tutorial_state(robot, current_user)
            if see_tutorial:
                put_next_state(STATE_TUTORIAL2)
            else:
                put_next_state(STATE_SHOW_MAP)
            
            print_end(STATE_TUTORIAL0)
        
        if state.state_name == STATE_TUTORIAL1:
            print_start(STATE_TUTORIAL1)
            
            handle_click_tutorial_state(robot, current_user)
            put_next_state(STATE_TUTORIAL2)
            
            print_end(STATE_TUTORIAL1)
        
        if state.state_name == STATE_TUTORIAL2:
            print_start(STATE_TUTORIAL2)
            
            handle_zoom_tutorial_state(robot, current_user)
            put_next_state(STATE_TUTORIAL3)
            
            print_end(STATE_TUTORIAL2)
        
        if state.state_name == STATE_TUTORIAL3:
            print_start(STATE_TUTORIAL3)
            
            handle_move_tutorial_state(robot, current_user)
            put_next_state(STATE_TUTORIAL4)
            
            print_end(STATE_TUTORIAL3)
        
        if state.state_name == STATE_TUTORIAL4:
            print_start(STATE_TUTORIAL4)
            
            handle_rotate_tutorial_state(robot, current_user)
            put_next_state(STATE_SHOW_MAP)            
            task2_end_time = time.time()
            task2_time = task2_end_time - task1_end_time
            
            print_end(STATE_TUTORIAL4)
        
        if state.state_name == STATE_SHOW_MAP:
            print_start(STATE_SHOW_MAP)
            
            handle_show_map_state(robot, current_user)
            put_next_state(STATE_CHOSE_LOCATION)
            
            print_end(STATE_SHOW_MAP)
            
        if state.state_name == STATE_CHOSE_LOCATION:
            print_start(STATE_CHOSE_LOCATION)
            
            task4_time, num_time = handle_chose_location_state(robot, current_user)
            put_next_state(STATE_EXIT)
            task3_end_time = time.time()
            task3_time = task3_end_time - task2_end_time
            
            print_end(STATE_CHOSE_LOCATION)
        
        elif state.state_name == STATE_EXIT:
            print_start(STATE_EXIT)
            
            handle_exit_state(robot, current_user)
            
            print_start(STATE_EXIT)
            break
    
collect_data(current_user.name, task1_time, task2_time, task3_time, task4_time, num_time, "./data.json")
robot.stop()