import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
from datetime import datetime

from matplotlib.widgets import Slider, Button
from slider import *

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



init_beta = 0.224
init_a = 3
init_gama = 0.212

graph = Graph("seir", g, T, N)

graph.add_parametr("beta", init_beta, 0, 1)
graph.add_parametr("a", init_a, 0, 3)
graph.add_parametr("gama", init_gama, 0, 1)

graph.preset()

