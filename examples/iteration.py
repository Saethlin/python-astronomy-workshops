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

arr = np.random.rand(4096*4096)

# Looping over indices as in other languages
start = time.time()
for i in range(arr.size):
    e = arr[i]
print('Looping over indices:', time.time()-start)

# Basic iteration
start = time.time()
for i in arr:
    pass
print('Proper for each use:', time.time()-start)