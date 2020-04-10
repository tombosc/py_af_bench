from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from numpy import get_include
from Cython.Distutils import build_ext
from filters_numba_aot import compile_aot

ext_modules = [
   Extension("filters_cython", sources=["filters_cython.pyx", "low_pass_test.c"])
]
setup(name="filters_cython", cmdclass={'build_ext': build_ext}, ext_modules=ext_modules)
compile_aot()
