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


#----------

throttle = np.zeros(100)
brake = np.zeros(100)
clutch = np.zeros(100)
steering = np.zeros(100)

#----------

def getThrottle():
    return random.randint(100)

def getBrake():
    return random.randint(100)

def getClutch():
    return random.randint(100)

def getSteering():
    return random.randint(100)

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
    
    start_time = time.time()
    z = 1 # displays the frame rate every 1 second
    counter = 0
    while 1:
        plt.cla()
        UpdateAll()
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
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
    #screen.close()


if __name__ == '__main__':
    main()