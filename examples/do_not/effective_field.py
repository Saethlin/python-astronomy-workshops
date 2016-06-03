"""
Compute the three-component effective H-field at each lattice point
Expects lmbda as an array with same shape as spin
"""
import numpy as np
from parameters import *
from magnet import magnet
from neighborsum import neighborsum

def effective_field(spin):
    #Components of the effecive H-field: exchange, anisotropy, demagnetization
    H_eff = (2 * J * neighborsum(spin)) + (2 * D * spin)
    
    if beta != 0:
        magnetization = magnet(spin)
        H_eff -= N * magnetization
    
    
    #Landau Damping
    if np.any(lmbda != 0):
        #I don't know why this is done twice, but that's how it was written in
        #the original FORTRAN code
        for repeat in range(2):
            dSdt = np.cross(spin,H_eff)
            H_eff -= lmbda * dSdt
        
    dSdt = np.cross(spin,H_eff)
    
    #boundary == 1 is a fixed boundary
    if boundary == 1:
        dSdt[edgemask] = 0
    
    return dSdt
