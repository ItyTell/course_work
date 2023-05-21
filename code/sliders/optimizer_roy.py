import numpy as np
import random

def diff(beta, gama, data, f):
    pass

def roy(f, n, N, iteration, w, a1, a2, A, B, eps):
    X = np.array([[random.uniform(A[i], B[i]) for i in range(n)] for j in range(N)])
    V = np.array([[random.uniform(-eps, eps) for i in range(n)] for j in range(N)])
    P = np.copy(X)
    res = np.array([f(X[i]) for i in range(N)])
    b = P[np.argmin(res)]
    for i in range(iteration):
        V = w * V + a1 * random.random() * (P - X) + a2 * random.random() * (b - X)
        X = X + V
        for j in range(N):
            res1 = f(X[j])
            if res1 < res[j]:
                P[j] = X[j]
                res[j] = res1
        b = P[np.argmin(res)]
    return b

def f(X):
    return 10 * X.shape[0] + np.sum(X*X - 10 * np.cos(2 * np.pi * X))

print(roy(f, 5, 100, 100000, 0.9, 1.5, 1.7, [-5.12 for i in range(10)], [5.12 for i in range(10)], 0.1))
