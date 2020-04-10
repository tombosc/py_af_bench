import time
import numpy as np
from numba import njit
from filters_cython import low_pass_pure_c, low_pass_pure_c_alloc, low_pass_cython
from filters_aot import numba_filter_aot
from base_filter import naive_filter, less_naive_filter, DTYPE

numba_filter = njit(naive_filter)
  
if __name__ == "__main__":
    alpha = 0.9
    # first verify that all functions yield same results
    # VERY important that numba_filter is called once before the timed 
    # benchmark, b/c the first call incurs big overhead due to jit compilation!
    x = np.random.randn(30).astype(np.float32)
    functions = [naive_filter, less_naive_filter, numba_filter, numba_filter_aot, low_pass_pure_c_alloc, low_pass_cython]
    names = ['numpy', 'numpy_2', 'numba', 'numba_aot', 'C', 'cython']
    prev_y = None
    for function, name in zip(functions, names):
        y = function(x, alpha)
        if prev_y is not None:
            assert(np.allclose(y, prev_y))
        prev_y = y
        print(y[:3]) # visual check in case...

    ranges = [100,500,1000]
    n_exps = 2000

    for fn, name in zip(functions, names):
        for T in ranges:
            x = np.random.randn(T).astype(DTYPE)
            begin = time.time()
            for _ in range(n_exps):
                y = fn(x, alpha)
            end = time.time()
            print(f"{name} on size {T} took {end-begin}")

    # In addition, what if we don't allocate memory at each call?
    functions = [low_pass_pure_c]
    names = ['C no alloc']

    for fn, name in zip(functions, names):
        y = np.empty(T, dtype=np.float32)
        for T in ranges:
            x = np.random.randn(T).astype(DTYPE)
            begin = time.time()
            for _ in range(n_exps):
                fn(x, y, alpha)
            end = time.time()
            print(f"{name} on size {T} took {end-begin}")
