"""
This is a short demonstration of the hazards that come from learning languages
like C/Java before Python; they promote ways of thinking that lead to painfully
slow code. If you're looping over an array in Python, you're almost always doing it wrong.

These loops work in C/Java because they are compiled. The compiler analyzes the program
as a whole and produces instructions for the CPU that may not resemble in any way the
code written. Python is interpreted and so there is no optimization as the interpreter
only sees one line at a time.
"""

import time
import numpy as np

arr = np.random.rand(4096, 4096)

# This is what you learn in C/Java
start = time.time()
arrsum = 0
for row in range(arr.shape[0]):
    for col in range(arr.shape[1]):
        arrsum += arr[row][col]
print(time.time()-start)

# The Python way
start = time.time()
arrsum = np.sum(arr)
print(time.time()-start)