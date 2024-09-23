import math
import threading

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
# 1.2m from start x coordinates (4 tiles) 23, 23+15

class Gesture:
    def __init__(self, app, robot):
        self.app = app
        self.motion = self.app.session.service("ALMotion")
        self.robot = robot
        self.start()

    def start(self):
        self.motion.wakeUp()
    
    def move_joints(self, joint_names, joint_values_grads, times, isAbsolute = True):
        self.motion.angleInterpolation(joint_names, [math.radians(joint_values_grad) for joint_values_grad in joint_values_grads], times, isAbsolute)

    def click_tutorial(self):
        joint_values = [-10, -40, 0, 60, 50]
        joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"]
        times = [3, 1.5, 2, 3.5, 1]
        self.move_joints(joint_names, joint_values, times)
        # times = [20, 20, 20, 20, 20]
        # self.move_joints(joint_names, joint_values, times)

    def zoom_tutorial(self):
        joint_values = [
            -10,  30,  50, 0,
            -10, -30, -50, 0
        ]
        joint_names = [
            "RShoulderPitch", "RElbowYaw", "RElbowRoll", "RHand",
            "LShoulderPitch", "LElbowYaw", "LElbowRoll", "LHand"
        ]
        times = [
            2, 2, 2, 2,
            2, 2, 2, 2
        ]
        self.move_joints(joint_names, joint_values, times)
        joint_values = [
            -45, -10,  30,  50, 0,
            45, -10, -30, -50, 0
        ]
        joint_names = [
            "RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RElbowRoll", "RHand",
            "LShoulderRoll", "LShoulderPitch", "LElbowYaw", "LElbowRoll", "LHand"
        ]
        times = [
            3, 3, 3, 3, 3,
            3, 3, 3, 3, 3
        ]
        self.move_joints(joint_names, joint_values, times)

    def move_tutorial(self):
        pass

    def rotate_tutorial(self):
        pass

    def show_map(self):
        self.show_map_start()
        threading.Thread(target=self._spown_map).start()
        while self.map_shown:
            joint_values = [10, -90, -90, 90]
            joint_names = ["LShoulderPitch", "LElbowYaw", "LWristYaw", "LHand"]
            times = [2, 2, 2, 2]
            self.move_joints(joint_names, joint_values, times)
        # times = [40, 40, 40, 40]
        # self.move_joints(joint_names, joint_values, times)
        # while self.map_shown:
        #     continue

    def show_map_start(self):
        self.map_shown = True

    def show_map_end(self):
        self.map_shown = False
        
    def _spown_map(self):
        joint_values = [-10, 89.5, 30, 60]
        joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        times = [2, 2, 2, 2]#, 2, 2, 2]
        self.move_joints(joint_names, joint_values, times)
        threading.Thread(target=self._spown_map_hand, args=(2,)).start()
        self.move_joints(joint_names, joint_values, times)
        
    def _spown_map_hand(self, total_time):
        joint_values = [90]
        joint_names = ["RHand"]
        time = 0.15
        times = [time]
        print(int((total_time/time)*2))
        for _ in range(int((total_time/time)/2)):
            joint_values = [90]
            self.move_joints(joint_names, joint_values, times)
            joint_values = [30]
            self.move_joints(joint_names, joint_values, times)

    def get_robot_position_orientation(self):
        position = self.motion.getRobotPosition(True)
        x, y, theta = position
        return {"x": x, "y": y, "theta": theta}
    
    def rotate(self, theta_target):
        theta_move = math.radians(theta_target) - self.get_robot_position_orientation()["theta"]
        self.motion.moveTo(0, 0, theta_move)

    def move_cartesian(self, x_target, y_target):
        x_move = x_target - self.get_robot_position_orientation()["x"]
        y_move = y_target - self.get_robot_position_orientation()["y"]
        self.motion.moveTo(x_move, y_move, 0)

    def move_to_zero(self):
        self.rotate(0)
        self.move_cartesian(0, 0)