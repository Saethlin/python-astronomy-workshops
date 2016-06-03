"""
Combine a set of fits images from file paths
"""
import numpy as np
from astropy.io import fits


def median_combine(filenames, hdu_index=0):
    for f, fname in enumerate(filenames):
        if f == 0:
            open_hdu = fits.open(fname)[hdu_index]
            # I construct the shape tuple by a one-item tuple with the shape of the first image
            stack = np.empty((len(filenames),) + open_hdu.data.shape)
            stack[f] = open_hdu.data
        else:
            stack[f] = fits.open(fname)[hdu_index].data

    # Overwrite input to save memory usage and some time; we don't care about stack so overwriting is safe
    return np.median(stack, axis=0, overwrite_input=True)
