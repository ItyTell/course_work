from slider import *
import ctypes
from ctypes import c_float, c_int, POINTER

sir = ctypes.CDLL("C:\\Users\\nickk\\course_work\\code\\sliders\\sir\\sir.so")
sir.sir.argtypes = [c_int, c_float, c_float, c_int, c_float]
sir.sir.restype = POINTER(c_float)

T = 1151
dt = 0.1
N = 647601

def g(beta, gama):
    size = int(T/dt)
    result = sir.sir(size, beta, gama, N, dt)
    answer = result[:T]
    sir.free_memory(result)
    return answer 

init_beta = 0.12
init_gama = 0.11

graph = Graph("sir", g, T, N)
graph.add_parametr("gama", init_gama, 0, 1)
graph.add_parametr("beta", init_beta, 0, 1)


graph.preset()