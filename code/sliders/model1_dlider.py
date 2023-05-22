import ctypes
from ctypes import c_float, c_int, POINTER
from slider_with_deth import *


name = "model1"
model1 = ctypes.CDLL(
    "C:\\Users\\nickk\\course_work\\code\\sliders\\"+ name+"\\"+name+".so")


model1.model1.argtypes = [
        c_int, 
        c_float, c_float, c_float, c_float, c_float, c_float, 
        c_float, c_float, c_float, c_float, c_float, c_float, 
        c_int, c_float]
model1.model1.restype = POINTER(POINTER(c_float))





T = 1151
dt = 0.1
N = 647601

def g(beta, beta1, l, p1, p2, a, gama_a, gama_i, gama_r, sigma_i, sigma_p, 
    sigma_h):
    size = int(T/dt)
    result = model1.model1(size, beta, beta1, l, p1, p2, a, 
            gama_a, gama_i, gama_r, sigma_i, sigma_p, sigma_h, N, dt)
    answer = result[0][:T]
    H = result[1][:T]
    F = result[2][:T]
    model1.free_memory(result)
    return answer, H, F 


init_beta = 0.224
init_beta1 = 0.1
init_l = 0.1
init_p1 = 0.9
init_p2 = 0.01
init_a = 3
init_gama_a = 0.212
init_gama_i = 0.212
init_gama_r = 0.212
init_sigma_i = 0.001
init_sigma_p = 0.001
init_sigma_h = 0.001


graph = Graph("model1", g, T, N)

graph.add_parametr("beta", init_beta, 0, 1)
graph.add_parametr("beta1", init_beta1, 0, 1)
graph.add_parametr("l", init_l, 0, 5)
graph.add_parametr("p1", init_p1, 0, 1)
graph.add_parametr("p2", init_p1, 0, 1)
graph.add_parametr("a", init_a, 0, 10)
graph.add_parametr("gama_a", init_gama_a, 0, 1)
graph.add_parametr("gama_i", init_gama_i, 0, 1)
graph.add_parametr("gama_r", init_gama_r, 0, 1)
graph.add_parametr("sigma_i", init_sigma_i, 0, 1)
graph.add_parametr("sigma_p", init_sigma_p, 0, 1)
graph.add_parametr("sigma_h", init_sigma_h, 0, 1)

graph.preset()

