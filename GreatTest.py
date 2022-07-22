from atexit import register
from random import random
from turtle import width
import pyformulas as pf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from scipy.ndimage.interpolation import shift
import numpy as np
from numpy import random
import time
import sys
import pygame
from pygame.locals import *

#----------

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

#----------

throttle = np.zeros(100)
brake = np.zeros(100)
clutch = np.zeros(100)
steering = np.zeros(100)

throttleval = 0
brakeval = 0
clutchval = 0
steeringval = 0

#----------

def setThrottle(val):
    global throttleval
    throttleval=val

def setBrake(val):
    global brakeval
    brakeval=val

def setClutch(val):
    global clutchval
    clutchval=val

def setSteering(val):
    global steeringval
    steeringval=val

#----------
def getThrottle():
    global throttleval
    return throttleval

def getBrake():
    global brakeval
    return brakeval

def getClutch():
    global clutchval
    return clutchval

def getSteering():
    global steeringval
    return steeringval

#----------

def UpdateThrottle():
    global throttle
    throttle = np.roll(throttle, -1)
    throttle[99] = getThrottle()

def UpdateBrake():
    global brake
    brake = np.roll(brake, -1)
    brake[99] = getBrake()

def UpdateClutch():
    global clutch
    clutch = np.roll(clutch, -1)
    clutch[99] = getClutch()

def UpdateSteering():
    global steering
    steering = np.roll(steering, -1)
    steering[99] = getSteering()

#----------

def ConvertAxis(val):
    if(val>=0):
        if(val % 10 != 1):
            return (val*100 % 100/2)+50
        else:
            return 100
    else:
        if(val % 10 != -1):
            return ((val*100 % 100)/2)
        else:
            return 0

def ConvertAxis2(val):
    return val % -96.8780517578125


def UpdateAll():
    UpdateThrottle()
    UpdateBrake()
    UpdateClutch()
    UpdateSteering()

def main():
    global throttle
    global brake
    global clutch
    global steering
    fig = plt.figure()
    screen = pf.screen(title='Plot')
    x = np.linspace(0, 100, 100)
    registered = False
    start_time = time.time()
    z = 1 # displays the frame rate every 1 second
    counter = 0
    stick = pygame.joystick.Joystick(0)
    stick.init()
    while 1:
        setThrottle(ConvertAxis2(stick.get_axis(5)))
        setBrake(ConvertAxis2(stick.get_axis(0)))
        print("Throttle: ", stick.get_axis(5))
        print("Brake: ", stick.get_axis(0))
        #if not registered:
            #setThrottle(0)

        UpdateAll()
        registered = False

        plt.cla()
        #UpdateAll()
        #plt.xlim(t-3,t)

        plt.plot(x, steering, c='black', linewidth=3) #nero
        plt.plot(x, throttle, c='#16f747', linewidth=3) #verde
        plt.plot(x, brake, c='blue', linewidth=3) #rosso, blu!?!
        plt.plot(x, clutch, c='r', linewidth=3) #blu, rosso!?!

        plt.ylim(0,100)
        plt.grid(False)
        plt.axis('off')
        #time.sleep(0.001)
        # If we haven't already shown or saved the plot, then we need to draw the figure first...
        fig.canvas.draw()

        image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        screen.update(image)

        counter+=1
        if (time.time() - start_time) > z :
            #print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
    #screen.close()


if __name__ == '__main__':
    main()