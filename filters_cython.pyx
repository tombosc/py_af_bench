# cython: language_level=3, boundscheck=False
import numpy as np
cimport numpy as np
from cython.view cimport array as cvarray

ctypedef np.float32_t DTYPE_t

cdef extern from "low_pass_test.h":
    int low_pass(float* x, float* y, int len, float alpha)
    np.ndarray[DTYPE_t, ndim=1] low_pass_alloc(float* x, int len, float alpha)


DTYPE = np.float32
def low_pass_pure_c(np.ndarray[DTYPE_t, ndim=1] x, np.ndarray[DTYPE_t, ndim=1] y, float alpha):
    low_pass(<float*>np.PyArray_DATA(x), <float*>np.PyArray_DATA(y), <int>x.shape[0], <float>alpha)
 
def low_pass_pure_c_alloc(np.ndarray[DTYPE_t, ndim=1] x, float alpha):
    cdef np.ndarray[DTYPE_t, ndim=1] y = np.zeros(x.shape[0] + 1, dtype=DTYPE)
    low_pass(<float*>np.PyArray_DATA(x), <float*>np.PyArray_DATA(y), <int>x.shape[0], <float>alpha)
    return y[1:]
   
def low_pass_cython(np.ndarray[DTYPE_t, ndim=1] x, float alpha):
    cdef np.ndarray[DTYPE_t, ndim=1] y = np.zeros(x.shape[0], dtype=DTYPE)
    y[0] = alpha * x[0]
    cdef int i = 1
    while i < x.shape[0]:
        y[i] = (1 - alpha) * y[i-1] + alpha * x[i]
        i = i + 1
    return y
