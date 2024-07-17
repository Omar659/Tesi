# Va cambiato tutto con funzioni del robot di ascolto, gesture e parlato
import sys
sys.path.append('./constants')
sys.path.append('./api')
from robot_constants import *
from api_call import *
import random
from datetime import datetime

def handle_hello_state(robot=None):
    pepper_question = random.choice(HELLO)
    print("Pepper:", pepper_question)
    while True:
        human_answer = input("You: ")
        response_hello = get_answer_hello(pepper_question, human_answer)
        if response_hello["understood"]:
            break
        print("Pepper:", response_hello["answer"])
    
    name_db = response_hello["answer_hidden"].lower()
    if get_user_exist(name_db):
        # mi tengo in un json il nome dell'utente. Non so se e meglio una classe dedicata o usare funzioni di robot.py
        user = get_user(name_db)
        days_passed = (datetime.now() - user.last_seen).days
        pepper_welcome_back_message = response_hello["answer"].replace("Welcome", "Welcome back")
        if days_passed > 1:
            pepper_welcome_back_message += ", " + random.choice(WELCOME_BACK)
        print(pepper_welcome_back_message, days_passed)
    else:
        print("Pepper:", response_hello["answer"])
        user = User(name_db, datetime.now())
        post_create_user(user)
        print(response_hello)
    return