import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
from datetime import datetime

from matplotlib.widgets import Slider, Button
from slider import *
import ctypes
from ctypes import c_float, c_int, POINTER

sir = ctypes.CDLL("C:\\Users\\nickk\\course_work\\code\\sliders\\sir\\sir.so")
sir.sir.argtypes = [c_int, c_float, c_float, c_int, c_float]
sir.sir.restype = POINTER(c_int)

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
    size = int(T/dt)
    result = sir.sir(size, beta, gama, N, dt)
    answer = result[:T]
    sir.free_memory(result)
    print(answer[1:10])
    return answer 



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



saveax = fig.add_axes([0.6, 0.025, 0.1, 0.04])
sve = Button(saveax, 'Save', hovercolor='0.975')

def save_params(event):
    name = "sir"
    file = open("C:\\Users\\nickk\\course_work\\code\\sliders\\"+ name +"_params.txt", 'w')
    for slider in Param.sliders:
        file.write(slider.name + " " + str(slider.slider.val) + "\n")
    file.close()

sve.on_clicked(save_params)



plt.show()