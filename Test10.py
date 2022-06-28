import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure()
for n in range(len(x)):
    plt.plot(x[:n], y[:n], color='k')
    plt.axis([0, 10, 0, 1])
    plt.show()