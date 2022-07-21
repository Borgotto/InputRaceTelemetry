import pyformulas as pf
import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()


screen = pf.screen(title='Plot')

start = time.time()
while True:
    t = time.time() - start
    x = np.linspace(t-3, t, 100)
    steering = np.sin(2*np.pi*x) + np.sin(3*np.pi*x)
    gas = np.sin(x)
    brake = np.cos(x)
    clutch = np.cos(x)+2

    plt.xlim(t-3,t)
    plt.ylim(-5,5)
    plt.plot(x, steering, c='black') #nero
    plt.plot(x, gas, c='#16f747') #verde
    plt.plot(x, brake, c='blue') #rosso, blu!?!
    plt.plot(x, clutch, c='r') #blu, rosso!?!
    
    plt.grid(False)
    plt.axis('off')

    # If we haven't already shown or saved the plot, then we need to draw the figure first...
    fig.canvas.draw()

    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    screen.update(image)
#screen.close()