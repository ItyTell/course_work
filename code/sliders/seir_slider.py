import ctypes
from ctypes import c_float, c_int, POINTER
from slider import *

seir = ctypes.CDLL("C:\\Users\\nickk\\course_work\\code\\sliders\\seir\\seir.so")
seir.seir.argtypes = [c_int, c_float, c_float, c_float, c_int, c_float]
seir.seir.restype = POINTER(c_float)
T = 1151
dt = 0.1
N = 647601

def g(beta, a, gama):
    size = int(T/dt)
    result = seir.seir(size, beta, a, gama, N, dt)
    answer = result[:T]
    seir.free_memory(result)
    return answer 

init_beta = 0.224
init_a = 0
init_gama = 0.212
graph = Graph("seir", g, T, N)
graph.add_parametr("beta", init_beta, 0, 1)
graph.add_parametr("a", init_a, 0, 9)
graph.add_parametr("gama", init_gama, 0, 1)

graph.preset()

