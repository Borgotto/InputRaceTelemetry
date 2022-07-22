import pyformulas as pf
import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()

ax = fig.add_subplot(1,1,1)

screen = pf.screen(title='Plot')


gas = np.zeros(100)

start = time.time()
count=0
while True:
    count+=1
    t = time.time() - start
    x = np.linspace(0, 100, 100)
    steering = np.sin(2*np.pi*x) + np.sin(3*np.pi*x)
    
    gas[count]=count
    brake = np.cos(x)
    clutch = np.cos(x)+2

    if(count==50):
        gas[range(0,50)]=0
    plt.cla()

    #plt.xlim(t-3,t)
    plt.ylim(0,100)
    plt.plot(x, steering, c='black') #nero
    plt.plot(x, gas, c='#16f747') #verde
    plt.plot(x, brake, c='blue') #rosso, blu!?!
    plt.plot(x, clutch, c='r') #blu, rosso!?!
    
    frame = plt.gca()
    frame.axes.get_yaxis().set_ticks([])

    for i in range(10):
        x = np.delete(x, i)
        steering = np.delete(steering, i)

    #plt.grid(False)
    #plt.axis('off')
    time.sleep(0.005)
    # If we haven't already shown or saved the plot, then we need to draw the figure first...
    fig.canvas.draw()

    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    screen.update(image)
#screen.close()