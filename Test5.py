import time
import psutil
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

i = 0
x, y = [], []

while True:
    x.append(i)
    y.append(i)

    ax.plot(x, y, color='b')

    fig.canvas.draw()

    ax.set_xlim(left=max(0, i - 50), right=i + 50)
    fig.show()
    plt.pause(0.05)
    i += 1