import numpy as np
import random

from tqdm import tqdm


def roy(f, n, N, iteration, w, a1, a2, A, B, eps, first):
    X = np.array([[random.uniform(A[i], B[i]) for i in range(n)] for j in range(N)])
    for i in range(n):
        X[0][i] = first[i]
    V = np.array([[random.uniform(-eps, eps) for i in range(n)] for j in range(N)])
    P = np.copy(X)
    res = np.array([f(X[i]) for i in range(N)])
    b = P[np.argmin(res)]
    for i in tqdm(range(iteration)):
        V = w * V + a1 * random.random() * (P - X) + a2 * random.random() * (b - X)
        X = X + V
        for j in range(N):
            res1 = f(X[j])
            if res1 < res[j]:
                P[j] = X[j]
                res[j] = res1
        b = P[np.argmin(res)]
    return b

