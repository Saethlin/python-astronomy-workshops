import time
import numpy as np
import numba


def loop_sum(arr):
    sum = 0
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            sum += arr[row, col]
    return sum


def numpy_sum(arr):
    return np.sum(arr)


@numba.jit(nopython=True)
def crude_numba_sum(arr):
    return np.sum(arr)


@numba.jit(nopython=True)
def numba_sum(arr):
    sum = 0
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            sum += arr[row, col]
    return sum


def speed_test(function, input, repeats=20):
    start = time.time()
    for repeat in range(repeats):
        function(input)
    return (time.time()-start)/repeats


if __name__ == '__main__':
    test = np.empty((4096, 4096))

    print('Simple loop time:', speed_test(loop_sum, test, repeats=1))

    print('Numpy time:', speed_test(numpy_sum, test))

    print('Initial crude numba time:', speed_test(crude_numba_sum, test, repeats=1))

    print('Later crude numba time:', speed_test(crude_numba_sum, test))

    print('Initial numba time:', speed_test(numba_sum, test, repeats=1))

    print('Later numba time:', speed_test(numba_sum, test))

