import ctypes
from ctypes import c_float, c_int, POINTER
from slider import *

seipr = ctypes.CDLL("C:\\Users\\nickk\\course_work\\code\\sliders\\seipr\\seipr.so")
seipr.seipr.argtypes = [c_int, c_float, c_float, c_float, c_float, c_float, c_int, c_float]
seipr.seipr.restype = POINTER(c_float)

T = 1151
dt = 0.1
N = 647601


def g(beta, beta1, p1, a, gama):
    size = int(T/dt)
    result = seipr.seipr(size, beta, beta1, p1, a, gama, N, dt)
    answer = result[:T]
    seipr.free_memory(result)
    return answer 


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

