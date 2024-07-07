# Va cambiato tutto con funzioni del robot di ascolto, gesture e parlato
import sys
sys.path.append('./constants')
from robot_constants import *
import random

def handle_hello_state(robot=None):
    print(random.choice(HELLO))
    name = input("DA SOSTITUIRE CON UN STT: ")
    
    return