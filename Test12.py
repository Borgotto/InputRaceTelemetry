import numpy as np
import matplotlib.pyplot as plt
import collections
import psutil

x=np.linspace(-3,3,100)
y1=np.sin(x)
y2=np.cos(x)
y3=1/(1+np.exp(-x))
y4=np.exp(x)


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

cpu = collections.deque(np.zeros(10))
ax = plt.plot(cpu)

#ax[0, 0].plot(x, y1)
ax.set_title("Sine function")
ax.axis('off')

plt.show()