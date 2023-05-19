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

def f1(s, e, i, p, r, beta, beta1, p1, a, gama):
    return -beta * s * i / N -beta1 * s * p / N

def f2(s, e, i, p, r, beta, beta1, p1, a, gama):
    return beta * s * i / N + beta1 * s * p / N - a * e

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
        P[i + 1] = P[i] + f4(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        R[i + 1] = R[i] + f5(S[i], E[i], I[i], P[i], R[i], beta, beta1, p1, a, gama) * dt
        if i % int(1 / dt) == 0:
            z = i // int(1 / dt) 
            result[z] = I[i + 1] + P[i + 1] + result[z - 1 if z > 0 else 0] 
    return result 


init_beta = 0.224
init_beta1 = 0.1
init_p1 = 0.9
init_a = 3
init_gama = 0.212


graph = Graph("seipr", g, T, N)

graph.add_parametr("beta", init_beta, 0, 1)
graph.add_parametr("beta1", init_beta1, 0, 1)
graph.add_parametr("p1", init_p1, 0, 1)
graph.add_parametr("a", init_a, 0, 10)
graph.add_parametr("gama", init_gama, 0, 1)

graph.preset()

