import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# my files
from optimizer_roy import *


class Param():

    def __init__(self, fig, label, init_val, min, max, n) -> None:
        self.ax = fig.add_axes([0.1, 0.4 - n * 0.03, 0.8, 0.02])
        self.slider = Slider(
                            ax=self.ax,
                            label=label,
                            valmin=min,
                            valmax=max,
                            valinit=init_val)
        self.name = label


class Graph():

    def __init__(self, name, f, T, N) -> None:
        self.fig, self.ax = plt.subplots(1, 2)
        self.n = 0
        self.params = []
        self.name = name
        self.function = f
        self.T = T
        self.N = N
        self.inits = []
        self.save = Button(self.fig.add_axes([0.6, 0.025, 0.1, 0.04]), 'Save', hovercolor='0.975')
        self.load = Button(self.fig.add_axes([0.7, 0.025, 0.1, 0.04]), 'Load', hovercolor='0.975')
        self.optimize = Button(self.fig.add_axes([0.5, 0.025, 0.1, 0.04]), 'Optimize', hovercolor='0.975')
        self.path = "C:\\Users\\nickk\\course_work\\code\\sliders\\"
    
    def add_parametr(self, label, init_val, min, max):
        self.params.append(Param(self.fig, label, init_val, min, max, self.n))
        self.inits.append(init_val)
        self.n += 1
    
    def set_params(self, params):
        for i in range(len(params)):
            self.params[i].slider.set_val(params[i])
    
    def save_params(self, event):
        data ={}
        for param in self.params:
            data[param.name] = param.slider.val
        with open(self.path + self.name +"_params.json", 'w') as file:
            json.dump(data, file, indent= 3)
        file.close()

    def load_params(self, event):
        with open(self.path + self.name +"_params.json") as file:
            file_content = file.read()
            file_content = json.loads(file_content)
            self.set_params(list(file_content.values()))
        file.close()

    def update(self, event):
        values = []
        for param in self.params:
            values.append(param.slider.val)
        
        I, H, F = self.function(*values)
        self.line_inf.set_ydata(I)
        self.line_death.set_ydata(F)
        self.fig.canvas.draw_idle()
    
    def diff(self, params):
        values = (param for param in params )
        I, H, F = self.function(*values)
        return np.sum((np.array(I) - self.data)**2) #+ np.sum((np.array(F) - self.deaths)**2) 

    def optimizing(self, event):
        A = [param.slider.valmin for param in self.params]
        B = [param.slider.valmax for param in self.params]
        first = [param.slider.val for param in self.params]
        new_val = roy(self.diff, n = len(self.params), N = 50, iteration = 100, w = 0.9, a1 = 1.5, a2 = 1.7, A = A, B = B, eps = 0.01, first = first)
        print(self.diff(new_val))
        self.set_params(new_val)
    
    def load_file(self):
        file = open("data.txt")
        self.data = file.readline().split()
        for i in range(len(self.data)):
            self.data[i] = int(self.data[i])
        file.close()
        self.data = np.array(self.data)
        
        file = open(r"C:\Users\nickk\course_work\code\deaths.txt")
        self.deaths = file.readline().split()
        for i in range(len(self.deaths)):
            self.deaths[i] = int(self.deaths[i])
        file.close()
        self.deaths = np.array(self.deaths)

    def drew(self):
        self.t = np.array([i for i in range(self.T)])
        I, H, F = self.function(*self.inits)

        self.line_inf, = self.ax[0].plot(self.t, I, lw=2)
        self.line_death, = self.ax[1].plot(self.t, F, lw=2)


        self.ax[0].plot(self.t, self.data, color='r')
        self.ax[0].set_xlabel('Time [d]')
        self.ax[0].set_title("I")

        self.ax[1].plot(self.t, self.deaths, color='r')
        self.ax[1].set_xlabel('Time [d]')
        self.ax[1].set_title("D")

        plt.ylim(0, self.N / 2)
        self.fig.subplots_adjust(bottom=0.5)
    
    def buttons(self):
        self.save.on_clicked(self.save_params)
        self.load.on_clicked(self.load_params)
        self.optimize.on_clicked(self.optimizing)
        for param in self.params:
            param.slider.on_changed(self.update)
        plt.show()

    def preset(self):
        self.load_file()
        self.drew()
        self.buttons()

