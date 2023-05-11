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

def f1(s, e, i, p, r, beta, beta1, p1, a, gama):
    return -beta * s * i / N -beta1 * s * p1 / N

def f2(s, e, i, p, r, beta, beta1, p1, a, gama):
    return beta * s * i / N + beta1 * s * p1 / N - a * e

def f3(s, e, i, p, r, beta, beta1, p1, a, gama):
    return a * p1 * e - gama * i 

def f4(s, e, i, p, r, beta, beta1, p1, a, gama):
    return a * (1 - p1) * e - gama * p

def f5(s, e, i, p, r, beta, beta1, p1, a, gama):
    return gama * (i + p)


def g(beta, beta1, p1, a, gama):
    S = np.zeros(int(T / dt) +1)
    E = np.zeros(int(T / dt) + 1)
    I = np.zeros(int(T / dt) + 1)
    P = np.zeros(int(T / dt) + 1)
    R = np.zeros(int(T / dt) + 1)
    result = np.zeros(T)
    
    S[0] = N -1
    I[0] = 1
    t = 0
    for i in range(int(T / dt)):
        t += dt
        S[i + 1] = S[i] + f1(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        E[i + 1] = E[i] + f2(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        I[i + 1] = I[i] + f3(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        P[i + 1] = P[i] + f3(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        R[i + 1] = R[i] + f5(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        if i % int(1 / dt) == 0:
            z = i // int(1 / dt) 
            result[z] = I[i + 1] + P[i + 1] + result[z - 1 if z > 0 else 0] 
    return result 



t = np.array([i for i in range(T)])

# Define initial parameters
init_beta = 0.224
init_beta1 = 0.1
init_p1 = 1
init_a = 3
init_gama = 0.212


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, g(init_beta, init_beta1, init_p1, init_a ,init_gama), lw=2)
ax.plot(t, data, color='r')
ax.set_xlabel('Time [d]')
plt.ylim(0, N / 2)

fig.subplots_adjust(bottom=0.5)

beta = Param(fig, 'beta', init_beta, 0, 1)

beta1 = Param(fig, 'beta1', init_beta1, 0, 1)

p1 = Param(fig, 'p1', init_p1, 0, 1)

a =          Param(fig, 'a', init_a, 0, 3)

gama = Param(fig, 'gama', init_gama, 0, 1)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(g(beta.slider.val, beta1.slider.val, p1.slider.val, a.slider.val, gama.slider.val))
    fig.canvas.draw_idle()

for slider in Param.sliders:
    slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    for slider in Param.sliders:
        slider.reset()
button.on_clicked(reset)

plt.show()