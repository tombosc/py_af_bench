from numba.pycc import CC
from base_filter import naive_filter
import numpy as np

cc = CC('filters_aot')
DTYPE=np.float32

# Normally, you would use cc.export as a decorator before function definition:
#@cc.export('numba_filter_aot', 'f4[:](f4[:], f4)')
# But I define the function only once this way
numba_filter_aot=cc.export('numba_filter_aot', 'f4[:](f4[:], f4)')(naive_filter)

def compile_aot():
    cc.compile()
