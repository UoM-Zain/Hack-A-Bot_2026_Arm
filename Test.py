import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, \
                                   QArmMiniFunctions
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer
import time

def PickUp(Arm):
    Arm.read_write_std(gripper=0.5333333333333)
    time.sleep(3)
    Arm.read_write_std(np.array([0, np.pi/13, -np.pi/2, 8*np.pi/9], dtype=np.float64), gripper=0.5333333333333)
    time.sleep(3)
    Arm.read_write_std(np.array([0, np.pi/13, -np.pi/2, 8*np.pi/9], dtype=np.float64), gripper=0)
    time.sleep(3)
    Arm.read_write_std(np.array([0, np.pi/13, -np.pi/2, 8*np.pi/9], dtype=np.float64), gripper=0.5333333333333)

def Main(arm = QArmMini(hardware=1, id=5)):
    kbd         = QKeyboard()
    groundPos   = np.array([0, np.pi/13, -np.pi/2, 8*np.pi/9-0.1], dtype=np.float64)
    kbdNav      = QArmMiniKeyboardNavigator(keyboard=kbd, initialPose=groundPos)
    myArmMath   = QArmMiniFunctions()
    timer       = QTimer(sampleRate=30.0, totalTime=300.0)
    clawPosition = 0
    edge = 0

        # main loop
    while timer.check() and not kbd.states[kbd.K_ESC]:
        kbd.update() 
    
        ##claw movement
        if kbd.states[kbd.K_LEFT]:
            clawPosition = 0
        if kbd.states[kbd.K_RIGHT]:
            clawPosition = 0.5333333333

        ## Section C - QArm Mini hardware I/O
        arm.read_write_std(
            kbdNav.move_joints_with_keyboard(timer.get_sample_time(), speed=np.pi/4), clawPosition)

        ## Section D - Record data for plotting
        pose, rotationMatrix, gamma = myArmMath.forward_kinematics(arm.positionMeasured)
        if kbd.states[kbd.K_SPACE]:
            if not edge:
                edge = 1
                PickUp(arm)
                #print("pose = "+str(pose)+"\nrotationMatrix = "+str(rotationMatrix) + "\ngamma = "+str(gamma))
        else:
            edge = 0
        

        timer.sleep()


Main()
