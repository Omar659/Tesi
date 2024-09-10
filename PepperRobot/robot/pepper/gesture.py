import math


# joint_names = [
#     "HeadYaw",
#     "HeadPitch",
#     "LShoulderPitch",
#     "LShoulderRoll",
#     "LElbowYaw",
#     "LElbowRoll",
#     "LWristYaw",
#     "LHand",
#     "HipRoll",
#     "HipPitch",
#     "KneePitch",
#     "RShoulderPitch",
#     "RShoulderRoll",
#     "RElbowYaw",
#     "RElbowRoll",
#     "RWristYaw",
#     "RHand",
#     "WheelFL",
#     "WheelFR",
#     "WheelB"
# ]
# 1.2m from start x coordinates (4 tiles)

class Gesture:
    def __init__(self, app):
        self.app = app
        self.motion = self.app.session.service("ALMotion")
        self.start()

    def start(self):
        self.motion.wakeUp()
    
    def move(self, joint_names, joint_values_grads, times, isAbsolute = True):
        self.motion.angleInterpolation(joint_names, [math.radians(joint_values_grad) for joint_values_grad in joint_values_grads], times, isAbsolute)

    def click_tutorial(self):
        joint_values = [-50, -70, 200]
        joint_names = ["RShoulderPitch", "RWristYaw", "RHand"]
        times = [3, 3, 3]
        self.move(joint_names, joint_values, times)
        print("SONO ENTRATO")