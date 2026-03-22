import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, \
                                   QArmMiniFunctions
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer
import time

def PickUp(Arm, currentPos = None, Height = 0, theta = np.pi /13,  ground = np.array([0, np.pi/13,   -np.pi/3 , np.pi/2], dtype=np.float64), angle = -np.pi/2):
    if currentPos != None:
        Arm.read_write_std(currentPos, gripper = 0.5333333333333)
        time.sleep(1.5)
    Arm.read_write_std(ground, gripper=0.5333333333333)
    time.sleep(1.5)
    Arm.read_write_std(ground, gripper=0)
    time.sleep(1.5)
    Arm.read_write_std(ground, gripper=0.5333333333333)
    time.sleep(1.5)
    Place(Arm, height = Height, theta= theta, angle = angle)

def Place(Arm, angle = -np.pi/2, theta = np.pi/13, height = 0):
    phi = (theta + (np.pi/2) - np.arccos(1.1097*np.sin(theta) + 0.456  - (height * 0.403)))
    arr = [angle, theta, -phi, (2*np.pi/2) - theta - phi]  
    above = [angle, np.pi/2, -phi, np.pi/2-theta+phi]
    position = np.array(arr, dtype=np.float64)
    Arm.read_write_std(above, gripper=0.5333333333333)
    time.sleep(1.5)
    Arm.read_write_std(position, gripper=0.5333333333333)
    time.sleep(1.5)
    Arm.read_write_std(position, gripper=0.4)
    time.sleep(1.5)
    Arm.read_write_std(np.array(above), gripper=0)
    time.sleep(1.5)

def standardPlace(arm, height):
    heightAngles = [np.pi/13, 0.48207, 0.68949, 0.75291]
    PickUp(arm, Height = height, theta= heightAngles[height])
    return height + 1

def Manual(position, keyboard, speed = 0.03):
    state = keyboard.states
    height = 0
    arr = [state[keyboard.K_A]-state[keyboard.K_D], state[keyboard.K_W]- state[keyboard.K_S]]
    position[0] = position[0] + (arr[0])
    position[1] = position[1] - (arr[1])
    position[2] = 0 #np.pi-((np.arccos(1.1097*np.sin(position[1]) + 0.376 - 0.323*height))+position[1])
    return position

def Main():
    mainArm = QArmMini(hardware=1, id=5)
    height = 0
    heightAngles = [np.pi/13, 0.48207, 0.68949, 0.75291]
    kbd         = QKeyboard()
    myArmMath   = QArmMiniFunctions()
    timer       = QTimer(sampleRate=30.0, totalTime=300.0)
    kbdNav      = QArmMiniKeyboardNavigator(keyboard=kbd, initialPose=mainArm.HOME_POSE)
    kbdNav      = QArmMiniKeyboardNavigator(keyboard=kbd, initialPose=mainArm.HOME_POSE)
    edge = 0

        # main loop
    while timer.check() and not kbd.states[kbd.K_ESC]:
        kbd.update() 
        
        mainArm.read_write_std(
            kbdNav.move_joints_with_keyboard(timer.get_sample_time(), speed=np.pi/4), 0)


        ## Section D - Record data for plotting
        pose, rotationMatrix, gamma = myArmMath.forward_kinematics(mainArm.positionMeasured)
        if kbd.states[kbd.K_SPACE]:
            if not edge:
                edge = 1
                PickUp(mainArm, kbdNav.move_joints_with_keyboard(timer.get_sample_time(), speed=np.pi/4), Height = height, theta= heightAngles[height])
                height = height + 1
        else:
            edge = 0
        

        timer.sleep()


Main()