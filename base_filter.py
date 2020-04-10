""" Define the naive numpy implem. of the filter. """

import numpy as np

DTYPE=np.float32

def naive_filter(x, alpha):
    y = np.empty(x.shape[0], dtype=DTYPE)
    y[0] = alpha * x[0]
    for i in range(1, len(x)):
        y[i] = (1-alpha) * y[i-1] + alpha * x[i]
    return y

def less_naive_filter(x, alpha):
    y = np.empty(x.shape[0], dtype=DTYPE)
    v = alpha * x[0]
    y[0] = v
    for i in range(1, len(x)):
        u = (1-alpha) * v + alpha * x[i]
        y[i] = u
        v = u
    return y


