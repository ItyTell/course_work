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

def f1(s, e, i, r, beta, a, gama):
    return -beta * s * i / N

def f2(s, e, i, r, beta, a, gama):
    return beta * s * i / N - a * e

def f3(s, e, i, r, beta, a, gama):
    return a * e - gama * i 

def f4(s, e, i, r, beta, a, gama):
    return gama * i

def g(beta, a, gama):
    S = np.zeros(int(T / dt) +1)
    E = np.zeros(int(T / dt) + 1)
    I = np.zeros(int(T / dt) + 1)
    R = np.zeros(int(T / dt) + 1)
    result = np.zeros(T)
    
    S[0] = N -1
    I[0] = 1
    t = 0
    for i in range(int(T / dt)):
        t += dt
        S[i + 1] = S[i] + f1(S[i], E[i], I[i], R[i], beta, a, gama) * dt
        E[i + 1] = E[i] + f2(S[i], E[i], I[i], R[i], beta, a, gama) * dt
        I[i + 1] = I[i] + f3(S[i], E[i], I[i], R[i], beta, a, gama) * dt
        R[i + 1] = R[i] + f4(S[i], E[i], I[i], R[i], beta, a, gama) * dt
        if i % int(1 / dt) == 0:
            z = i // int(1 / dt) 
            result[z] = I[i + 1] + result[z - 1 if z > 0 else 0] 
    return result 



t = np.array([i for i in range(T)])

init_beta = 0.224
init_a = 3
init_gama = 0.212

fig, ax = plt.subplots()
line, = ax.plot(t, g(init_beta, init_a ,init_gama), lw=2)
ax.plot(t, data, color='r')
ax.set_xlabel('Time [d]')
plt.ylim(0, N / 2)

fig.subplots_adjust(bottom=0.5)

beta = Param(fig, 'beta', init_beta, 0, 1)

a =          Param(fig, 'a', init_a, 0, 3)

gama = Param(fig, 'gama', init_gama, 0, 1)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(g(beta.slider.val, a.slider.val, gama.slider.val))
    fig.canvas.draw_idle()


for slider in Param.sliders:
    slider.on_changed(update)

resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    for slider in Param.sliders:
        slider.reset()



button.on_clicked(reset)

plt.show()