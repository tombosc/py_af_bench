# Simple benchmark of C integration into python for real-time audio filtering 

Requires numpy, numba and cython. Based on this [nice blogpost (Bastian Bechtold)](https://bastibe.de/2012-11-02-real-time-signal-processing-in-python.html). I compare python with numpy with cython (both using cython half-C half-python language and real C code), numba (both with just-in-time compilation and ahead-of-time compilation).

To compile modules that should be compiled:

```python setup.py build_ext```

To run the test:

```python test_filters.py```

The filter is defined by the recurrence `y[n] = (1-alpha) y[n-1] + alpha x[n]`. AFAIK, in numpy, this has to be a for loop. Using C code, it is at least 500 times faster.

The arrays used have size between 100 and 1000 which corresponds to reasonable real-time audio buffer size. To get sufficient reactivity (short delay between keypress and sound), you want to split each beat in, say 24\*4 (24 pulse-per-quarter note as in the MIDI standard) and generate pieces of soundwaves. At 120 BPM, that's 24\*4\*2=192 per sec, so if your resolution is 44100Hz, you'll approximately generate 230 samples at each call. 

The code is naive and could be further improved (even in the C version). Also, we could get rid of memory allocations (I compare the 2 C versions w/ and w/o memory alloc for storing the results).

# My results

```
numpy on size 100 took 1.0655884742736816
numpy on size 500 took 5.286687850952148
numpy on size 1000 took 10.558638334274292
numpy_2 on size 100 took 0.5905225276947021
numpy_2 on size 500 took 2.866945743560791
numpy_2 on size 1000 took 5.741191148757935
numba on size 100 took 0.002925872802734375
numba on size 500 took 0.008173465728759766
numba on size 1000 took 0.016030073165893555
numba_aot on size 100 took 0.003183126449584961
numba_aot on size 500 took 0.009852170944213867
numba_aot on size 1000 took 0.01680898666381836
C on size 100 took 0.007919549942016602
C on size 500 took 0.008340597152709961
C on size 1000 took 0.015307188034057617
cython on size 100 took 0.01210165023803711
cython on size 500 took 0.01411747932434082
cython on size 1000 took 0.02516627311706543
C no alloc on size 100 took 0.0026319026947021484
C no alloc on size 500 took 0.005041837692260742
C no alloc on size 1000 took 0.0071430206298828125
```
