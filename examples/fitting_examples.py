import time
import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt


def rms(data, model):
    return np.sqrt(np.mean((data - model)**2))


def gaussian(x, height, center, width):
    return height*np.exp(-(center - x)**2 / (2*width**2))


def voigt(x, height, center, gauss_width, lorentz_width):
    dst = x-center
    z = (dst+(abs(lorentz_width)*1j))/(abs(gauss_width)*np.sqrt(2))

    return height * scipy.special.wofz(z).real/(abs(gauss_width)*np.sqrt(2*np.pi))


true_params = (1e4, 0, 20, 20)
npts = 1e5

xdata = np.linspace(-100, 100, npts)
ydata = voigt(xdata, *true_params) + np.random.randn(xdata.size)
print('true rms:', rms(ydata, voigt(xdata, *true_params)))
print()

# Polynomial model
start = time.time()
coefficients = np.polyfit(xdata, ydata, 10)
print('poly time:', time.time()-start)

poly_fit = np.polyval(coefficients, xdata)
print('poly rms:', rms(poly_fit, ydata))
print()

# Gaussian model
start = time.time()
model = scipy.optimize.curve_fit(gaussian, xdata, ydata, p0=[100,0,20])[0]
print('gaussian time:', time.time()-start)

gaussian_fit = gaussian(xdata, *model)
print('gaussian rms:', rms(gaussian_fit, ydata))
print()

# Voigt model
start = time.time()
model, _ = scipy.optimize.curve_fit(voigt, xdata, ydata)
print('voigt time:', time.time()-start)

voigt_fit = voigt(xdata, *model)
print('voigt rms:', rms(voigt_fit, ydata))
print()

plt.plot(xdata, ydata, 'k.')
plt.plot(xdata, poly_fit, color='b', lw=3)
plt.plot(xdata, gaussian_fit, color='r', lw=3)
plt.plot(xdata, voigt_fit, color='y', lw=3)
plt.show()