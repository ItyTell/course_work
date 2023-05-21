
from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
import numpy as np
import json
from optimizer_roy import *

class Param():


    def __init__(self, fig, label, init_val, min, max, n) -> None:
        self.ax = fig.add_axes([0.1, 0.4 - n * 0.05, 0.8, 0.02])
        self.slider = Slider(
                            ax=self.ax,
                            label=label,
                            valmin=min,
                            valmax=max,
                            valinit=init_val)
        self.name = label
    

class Graph():

    def __init__(self, name, f, T, N) -> None:
        self.fig, self.ax = plt.subplots()
        self.n = 0
        self.params = []
        self.name = name
        self.function = f
        self.T = T
        self.N = N
        self.inits = []
        self.save = Button(self.fig.add_axes([0.6, 0.025, 0.1, 0.04]), 'Save', hovercolor='0.975')
        self.load = Button(self.fig.add_axes([0.7, 0.025, 0.1, 0.04]), 'Load', hovercolor='0.975')
        self.rest = Button(self.fig.add_axes([0.8, 0.025, 0.1, 0.04]), 'Reset', hovercolor='0.975')
        self.optimize = Button(self.fig.add_axes([0.5, 0.025, 0.1, 0.04]), 'Optimize', hovercolor='0.975')
    
    def add_parametr(self, label, init_val, min, max):
        self.params.append(Param(self.fig, label, init_val, min, max, self.n))
        self.inits.append(init_val)
        self.n += 1
    
    def save_params(self, event):
        data ={}
        for param in self.params:
            data[param.name] = param.slider.val
        with open("C:\\Users\\nickk\\course_work\\code\\sliders\\"+ self.name +"_params.json", 'w') as file:
            json.dump(data, file, indent= 3)

    def load_params(self, event):
        with open("C:\\Users\\nickk\\course_work\\code\\sliders\\"+ self.name +"_params.json") as file:
            file_content = file.read()
            file_content = json.loads(file_content)
        for i, value in enumerate(file_content.values()):
            self.params[i].slider.set_val(value)


    def reset(self, event):
        for param in self.params:
            param.slider.reset()
    
    def update(self, event):
        values = []
        for param in self.params:
            values.append(param.slider.val)
        self.line.set_ydata(self.function(*values))
        self.fig.canvas.draw_idle()
    
    def diff(self, params):
        values = (param for param in params )
        return np.sum((np.array(self.function(*values)) - self.data)**2)

    def optimizing(self, event):
        n = len(self.params)
        N = 50
        iteration = 100
        w = 0.9
        a1 = 1.5
        a2 = 1.7
        A = [param.slider.valmin for param in self.params]
        B = [param.slider.valmax for param in self.params]
        eps = 0.01
        first = [param.slider.val for param in self.params]
        new_val = roy(self.diff, n, N, iteration, w, a1, a2, A, B, eps, first)
        for i in range(len(self.params)):
            self.params[i].slider.set_val(new_val[i])

    
    def preset(self):
        file = open("data.txt")
        self.data = file.readline().split()
        for i in range(len(self.data)):
            self.data[i] = int(self.data[i])
        file.close()
        self.data = np.array(self.data)

        self.t = np.array([i for i in range(self.T)])

        self.ax.plot(self.t, self.data, color='r')

        self.line, = self.ax.plot(self.t, self.function(*self.inits), lw=2)

        self.ax.set_xlabel('Time [d]')
        plt.ylim(0, self.N / 2)
        self.fig.subplots_adjust(bottom=0.5)

        self.save.on_clicked(self.save_params)
        self.load.on_clicked(self.load_params)
        self.rest.on_clicked(self.reset)
        self.optimize.on_clicked(self.optimizing)
        for param in self.params:
            param.slider.on_changed(self.update)
        plt.show()





