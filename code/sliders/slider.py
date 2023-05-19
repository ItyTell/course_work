
from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
import numpy as np
import json

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
        self.reset = Button(self.fig.add_axes([0.8, 0.025, 0.1, 0.04]), 'Reset', hovercolor='0.975')
    
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

    
    def preset(self):
        file = open("data.txt")
        data = file.readline().split()
        for i in range(len(data)):
            data[i] = int(data[i])
        file.close()

        self.t = np.array([i for i in range(self.T)])

        self.ax.plot(self.t, data, color='r')

        self.line, = self.ax.plot(self.t, self.function(*self.inits), lw=2)

        self.ax.set_xlabel('Time [d]')
        #plt.ylim(0, self.N / 2)
        self.fig.subplots_adjust(bottom=0.5)

        self.save.on_clicked(self.save_params)
        self.load.on_clicked(self.load_params)
        self.reset.on_clicked(self.reset)
        for param in self.params:
            param.slider.on_changed(self.update)
        plt.show()





