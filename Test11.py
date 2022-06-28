import matplotlib.pyplot as plt

#define data
x = [3, 4, 4, 6, 7, 8, 8, 12]
y = [11, 12, 12, 14, 17, 15, 14, 19]

#create scatterplot
plt.scatter(x, y)

#get current axes
ax = plt.gca()

#hide axes and borders
plt.axis('off')