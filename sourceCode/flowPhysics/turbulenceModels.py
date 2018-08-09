# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:33:34 2018

@author: root
"""

import numpy as np
import matplotlib.pyplot as plt


def TKE(U,I):
    """
    Turbulent kinetic energy
    """
    k = 3*(U*I)**2/2
    return k

def omega(k, l):
    """
    Relation for the specific turbulent dissipation rate.   
    """
    omega = np.sqrt(k)/l
    return omega
    
def turbIntensity(k, U):
    """
    The turbulent intensity as a function of the velocity and TKE
    """
    I = 100*np.sqrt(2*k/3)/U
    return I 
    
def Flength(ReThetat):
    """
    Empirical relation for the 
    """
    if ReThetat<400:
        Flength = 398.189e-1 - 119.270e-4*ReThetat - 132.567e-6*ReThetat**2
    elif ReThetat<596:
        Flength = 263.404 - 123.939e-2*ReThetat + 194.548e-5*ReThetat**2 - 101.695e-8*ReThetat**3
    elif ReThetat<1200:
        Flength = (0.5 - (ReThetat - 596.0)*3.e-4)
    else:
        Flength = 0.3188
    return Flength
    
    
def Flambda(lambdaT, I):
    """
    Relation for the based on the pressure gradient parameter LambdaT and the turbulence intensity
    """
    if lambdaT<=0:
        Flambda = 1 - (-12.986*lambdaT - 123.66*lambdaT**2 - 405.689*lambdaT**3)*np.exp((I/1.5)**1.5)
    if lambdaT>0:
        Flambda = 1+ 0.275*(1-np.exp(-35*lambdaT))*np.exp(I/1.5)
    return Flambda
    
def ReThetat(I, lambdaT):
    """
    Transition onset momentum-thickness Reynolds number (for freestream conditions)
    """
    F = Flambda(lambdaT, I)
    if I<=1.3:
        ReThetat= (1173.51-589.428*I + 0.2196/I**2)*F
    else:
        ReThetat = 331.5*(I - 0.5658)**(-0.671*F)
    if I<0.027:
        print('take caution, the tubulence intensity is too low for the emperical relation')
    if ReThetat<20:
        print('take caution, the ReTheta is too low for the emperical relation')
    if lambdaT<-0.1:
        print('take caution, lambdaT is too small')
    elif lambdaT>0.1:
        print('take caution, lambdaT is too large')
    return ReThetat
    
    
    
    
if __name__=="__main__":
    I = 0.027
    lambdaT = 0
    ReThetat = ReThetat(I, lambdaT)
    print(ReThetat)
    startRange = 0.001
    endRange = 6.;    
    
    x = np.linspace(startRange, endRange, 1000)
    y = np.zeros(len(x))    
    for i in range(len(x)):
        y[i] = ReThetat(x[i], 0)
    plt.plot(x, y)
    plt.show()