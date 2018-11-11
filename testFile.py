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
from writeFunctions import writeHeader
import numpy as np



classType = 'dictionary'
f = open("test/testDict", 'w')
writeHeader(f, 'blockMeshDict', classType)
f.close()


