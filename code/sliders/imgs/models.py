import numpy as np
import matplotlib.pyplot as plt
import ctypes
from ctypes import c_float, c_int, POINTER


name = "model1"
model1 = ctypes.CDLL(
    "C:\\Users\\nickk\\course_work\\code\\sliders\\"+ name+"\\"+name+".so")
func = model1.model1 

func.argtypes = [
        c_int, 
        c_float, c_float, c_float, c_float, c_float, c_float, 
        c_float, c_float, c_float, c_float, c_float, c_float, 
        c_int, c_float]
func.restype = POINTER(POINTER(c_float))
T = 365
T1 = 50
dt = 0.1
N = 647601

def g(beta, beta1, l, p1, p2, a, gama_a, gama_i, gama_r, sigma_i, sigma_p, sigma_h):
    size = int((T + T1)/dt)
    result = func(size, beta, beta1, l, p1, p2, a, 
            gama_a, gama_i, gama_r, sigma_i, sigma_p, sigma_h, N, dt)
    answer = result[0][:T + T1]
    H = result[1][:T + T1]
    F = result[2][:T + T1]
    model1.free_memory(result)
    return answer 

beta = 0.887
beta1 = 0.369
l = 2.198
p1 = 0.652
p2 = 0.012
a = 2.84
gama_a = 0.155
gama_i = 0.34
gama_r = 0.492
sigma_i = 0.31
sigma_p = 0.723
sigma_h = 0.234

file = open("C:\\Users\\nickk\\course_work\\data.txt")
data = file.readline().split()
for i in range(len(data)):
    data[i] = int(data[i])
file.close()
data = np.array(data)

t = np.array([i for i in range(T + T1)])
fig, ax = plt.subplots()
ax.plot(t, data[:T + T1], color='r')
#line, = ax.plot(t, g(beta, beta1, l, p1, p2, a, gama_a, gama_i, gama_r, sigma_i, sigma_p, sigma_h)[: T + T1], lw=2)
ax.set_xlabel('Time [d]')
plt.axvline(x = T, color = 'black')
plt.savefig("imgs/data")
plt.show()
#plt.ylim(0, N )