#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 10:13:00 2018

@author: qlayerspc
"""
import os
from shieldflow.shieldFlow import findShieldCases, cleanCorruptCases
from foamFunctions import checkIfExist
from foamFunctions import getSolverPIDs, getActiveDirs
import numpy as np

directory = '/media/qlayerspc/DATA/Linux/OpenFOAM/run/spray/shieldFlow/optimization'
caseDict = findShieldCases(directory)
#print(caseDict)
os.chdir('/media/qlayerspc/DATA/Linux/OpenFOAM/run/spray/shieldFlow/optimization')

cleanCorruptCases(directory)
        
        
#for folder in os.listdir():
#    if folder.startswith('B150'):
#        checkStatus = checkIfExist(folder)
#        if checkStatus==1:
#            print(folder)
#            activeFoamCases = getActiveDirs('sprayFoam')
#            if folder in activeFoamCases:
#                caseDict[folder]=1
#            else:       # case is not running neither finished, so corrupt
#                caseDict[folder]=2       
#        else:       # case is fine
#            caseDict[folder]=0
#        
#solver = 'sprayFoam'
#PIDS = getSolverPIDs(solver)
#activeDirs = getActiveDirs(solver)
#print(activeDirs)