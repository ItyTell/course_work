
import numpy as np
import matplotlib.pyplot as plt
import ctypes
from ctypes import c_float, c_int, POINTER


seir = ctypes.CDLL("C:\\Users\\nickk\\course_work\\code\\sliders\\seir\\seir.so")
seir.seir.argtypes = [c_int, c_float, c_float, c_float, c_int, c_float]
seir.seir.restype = POINTER(c_float)
T = 365
T1 = 50
dt = 0.1
N = 647601


def g(beta, a, gama):
    size = int((T + T1)/dt)
    result = seir.seir(size, beta, a, gama, N, dt)
    answer = result[:T + T1]
    seir.free_memory(result)
    return answer 

beta = 0.645 
a = 9.756
gama = 0.613

file = open("C:\\Users\\nickk\\course_work\\data.txt")
data = file.readline().split()
for i in range(len(data)):
    data[i] = int(data[i])
file.close()
data = np.array(data)

t = np.array([i for i in range(T + T1)])
fig, ax = plt.subplots()
ax.plot(t, data[:T + T1], color='r')
line, = ax.plot(t, g(beta, a, gama)[: T + T1], lw=2)
ax.set_xlabel('Time [d]')
plt.axvline(x = T, color = 'black')
plt.savefig("imgs/SEIR365")
plt.show()
#plt.ylim(0, N )