import time
import numpy as np
import numba
import numexpr as ne


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


def numpy_expression(arr):
    return 2*arr + 3*arr + 4*arr + 5*arr


def numexpr_expression(arr):
    return ne.evaluate('2*arr + 3*arr + 4*arr + 5*arr')


@numba.jit(nopython=True)
def numba_expression(arr):
    return 2*arr + 3*arr + 4*arr + 5*arr



def speed_test(function, input, repeats=20):
    start = time.time()
    for repeat in range(repeats):
        function(input)
    return (time.time()-start)/repeats


if __name__ == '__main__':
    test = np.empty((4096, 4096))

    print('Simple loop time:', speed_test(loop_sum, test, repeats=1))
    print('Numpy time:', speed_test(numpy_sum, test))
    print()

    print('Initial crude numba time:', speed_test(crude_numba_sum, test, repeats=1))
    print('Later crude numba time:', speed_test(crude_numba_sum, test))
    print()

    print('Initial numba time:', speed_test(numba_sum, test, repeats=1))
    print('Later numba time:', speed_test(numba_sum, test))
    print()

    print('Long expression examples examples:')
    print('Normal Python/numpy:', speed_test(numpy_expression, test))
    print('Initial numba expression:', speed_test(numba_expression, test, repeats=1))
    print('Later numba expression:', speed_test(numba_expression, test))
    print('Numexpr:', speed_test(numexpr_expression, test))