import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow

def make_fig():
    plt.scatter(x, y)  # I think you meant this

plt.ion()  # enable interactivity
fig = plt.figure()  # make a figure

x = list()
y = list()

i=0
while True : 
    temp_y = np.random.random()
    x.append(i)
    y.append(temp_y)  # or any arbitrary update to your figure's data

    while(len(plt.addedData) > 0):
        y = np.roll(y, -1)
        y[-1] = plt.addedData[0]
        del(plt.addedData[0])

    i += 1
    drawnow(make_fig)