import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
from datetime import datetime

from matplotlib.widgets import Slider, Button


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

# Define initial parameters
init_beta = 0.224
init_gama = 0.212
init_a = 3

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, g(init_beta, init_a ,init_gama), lw=2)
ax.plot(t, data, color='r')
ax.set_xlabel('Time [d]')
plt.ylim(0, N / 2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.4)

# Make a horizontal slider to control the frequency.
axgama = fig.add_axes([0.25, 0.25, 0.65, 0.03])
gama_slider = Slider(
    ax=axgama,
    label='gama',
    valmin=0,
    valmax=1,
    valinit=init_gama,
)
axa = fig.add_axes([0.25, 0.1, 0.65, 0.03])
a_slider = Slider(
    ax=axa,
    label='a',
    valmin=0,
    valmax=3,
    valinit=init_a,
)

# Make a vertically oriented slider to control the amplitude
axbeta = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
beta_slider = Slider(
    ax=axbeta,
    label="beta",
    valmin=0,
    valmax=1,
    valinit=init_beta,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(g(beta_slider.val, a_slider.val, gama_slider.val))
    fig.canvas.draw_idle()


# register the update function with each slider
gama_slider.on_changed(update)
a_slider.on_changed(update)
beta_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    gama_slider.reset()
    a_slider.reset()
    beta_slider.reset()
button.on_clicked(reset)

plt.show()