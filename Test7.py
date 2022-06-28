import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import psutil
import collections

# function to update the data
def my_function(i):
    # get data
    cpu.popleft()
    cpu.append(psutil.cpu_percent())
    # clear axis
    ax.cla()
    # plot cpu
    ax.plot(cpu)
    ax.scatter(len(cpu)-1, cpu[-1])
    ax.set_ylim(0,100)
# start collections with zeros
cpu = collections.deque(np.zeros(10))
# define and adjust figure
fig = plt.figure(figsize=(12,6), facecolor='#FFFFFF')
ax = plt.subplot(121)
ax.set_facecolor('#DEDEDE')
# animate
ani = FuncAnimation(fig, my_function, interval=50)
plt.show()