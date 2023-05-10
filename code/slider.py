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



# The parametrized function to be plotted
def f(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)

t = np.array([i for i in range(T)])

# Define initial parameters
init_beta = 0.3
init_gama = 0.2

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, g(init_beta, init_gama), lw=2)
ax.plot(t, data, color='r')
ax.set_xlabel('Time [d]')
plt.ylim(0, N / 2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axgama = fig.add_axes([0.25, 0.1, 0.65, 0.03])
gama_slider = Slider(
    ax=axgama,
    label='gama',
    valmin=0,
    valmax=1,
    valinit=init_gama,
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
    line.set_ydata(g(beta_slider.val, gama_slider.val))
    fig.canvas.draw_idle()


# register the update function with each slider
gama_slider.on_changed(update)
beta_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    gama_slider.reset()
    beta_slider.reset()
button.on_clicked(reset)

plt.show()