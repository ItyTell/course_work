import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
from datetime import datetime

from matplotlib.widgets import Slider, Button
from slider import *



f = open("data.txt")
data = f.readline().split()
for i in range(len(data)):
    data[i] = int(data[i])

T = 1151
dt = 0.1
N = 647601

def f1(s, i, r, beta, gama):
    return -beta * s * i / N

def f2(s, i, r, beta, gama):
    return beta * s * i / N - gama * i

def f3(s, i, r, beta, gama):
    return gama * i

def g(beta, gama):
    S = np.zeros(int(T / dt) +1)
    I = np.zeros(int(T / dt) + 1)
    R = np.zeros(int(T / dt) + 1)
    result = np.zeros(T)
    
    S[0] = N -1
    I[0] = 1
    t = 0
    for i in range(int(T / dt)):
        t += dt
        S[i + 1] = S[i] + f1(S[i], I[i], R[i], beta, gama) * dt
        I[i + 1] = I[i] + f2(S[i], I[i], R[i], beta, gama) * dt
        R[i + 1] = R[i] + f3(S[i], I[i], R[i], beta, gama) * dt
        if i % int(1 / dt) == 0:
            z = i // int(1 / dt) 
            result[z] = I[i + 1] + result[z - 1 if z > 0 else 0] 
    return result 



t = np.array([i for i in range(T)])

init_beta = 0.12
init_gama = 0.11

fig, ax = plt.subplots()
line, = ax.plot(t, g(init_beta, init_gama), lw=2)
ax.plot(t, data, color='r')
ax.set_xlabel('Time [d]')
plt.ylim(0, N / 2)

fig.subplots_adjust(bottom=0.5)

gama = Param(fig, 'gama', init_gama, 0, 1)

beta = Param(fig, 'beta', init_beta, 0, 1)


def update(val):
    line.set_ydata(g(beta.slider.val, gama.slider.val))
    fig.canvas.draw_idle()

gama.slider.on_changed(update)
beta.slider.on_changed(update)

resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    gama.slider.reset()
    beta.slider.reset()
button.on_clicked(reset)

plt.show()