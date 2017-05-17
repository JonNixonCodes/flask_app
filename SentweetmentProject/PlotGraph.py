import matplotlib
matplotlib.use('TkAgg') # NEED THIS FOR VIRTUALENV

import matplotlib.pyplot as plt
import numpy as np

# makes an animation by repeatedly calling func
import matplotlib.animation as animation

#fig, ax = plt.subplots()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

data = []    

def UpdatePlot(i):
    graph_data = open('graph_data.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax.clear()
    ax.plot(xs, ys)

ani = animation.FuncAnimation(fig, UpdatePlot, interval=1000)
plt.show()
