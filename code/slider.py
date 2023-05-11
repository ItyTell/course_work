
from matplotlib.widgets import Slider, Button

class Param():

    n = 0
    sliders = []

    def __init__(self, fig, label, init_val, min, max) -> None:
        self.ax = fig.add_axes([0.1, 0.4 - Param.n * 0.05, 0.8, 0.02])
        self.slider = Slider(
                            ax=self.ax,
                            label=label,
                            valmin=min,
                            valmax=max,
                            valinit=init_val)
        Param.n += 1
        Param.sliders.append(self.slider)


