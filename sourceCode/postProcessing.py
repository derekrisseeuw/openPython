# -*- coding: utf-8 -*-
"""
file with fuctions to interact with openfoam 
"""

import numpy as np
import os
import re
from foamFunctions import getTimeFolders


def getParticlesFromLog(line):
    try:
        noParticles = int(line.split(' ')[-2].split(',')[0])
    except:
        noParticles = int(line.split(' ')[-1].split(',')[0])        #for total number
    return noParticles

def getActiveParticles(foamCase, time=-1):
    """
    Print the number of total and active particles in the flow. Time is optional, default latest timestep.    
    """
    timeFolders = getTimeFolders(foamCase)
    path = foamCase + '/' +timeFolders[time] + '/lagrangian/sprayCloud/active'
    f = open(path)
    data = f.readlines()
    f.close()  
    
    nTot = 17
    searchTotNumber = True 
    while searchTotNumber:
        totLine= data[nTot]
        if len(totLine)>1:
            searchTotNumber=False
        else:
            nTot+=1
            
    if '{' in totLine:
        totParticles = int(totLine.split('{')[0])
        activeParticles = totParticles
    else:
        activeParticles = 0
        totParticles = int(totLine)
        for i in range(nTot+2,len(data)):
            try:
                activeParticles = activeParticles + int(data[i])
            except:
                pass  
    return [totParticles, activeParticles]
    
def initializeParticlePositions(logFile, noPatches):
    """
    Initilization which finds the patches and type of local interaction
    """
    patchNames = []
    patchTypes = ['escape']*noPatches

#    initialize
    f = open(logFile)
    foundPatchNames = False
    foundPatchTypes = False
    lookForStick = False
    iPatch=-1
    while (not foundPatchNames) or (not foundPatchTypes):  
        line = f.readline()
        if 'Parcel fate: patch' in line:
            patchName = line.split(' ')[-3]
            patchNames.append(patchName)

            
        if lookForStick and 'stick' in line:
            patchTypes[len(patchNames)-1] = 'stick'
            if iPatch==noPatches:
                foundPatchTypes=True
        
        if 'escape' in line:
            lookForStick=True
            iPatch += 1
        else:
            lookForStick=False
            
        if len(patchNames)==noPatches:
            foundPatchNames=True

    return patchNames
        
    
    
def getParticlePositions(foamCase, noPatches):
    """
    This function evaluates the log file of the foamCase and gives the amount of particles that 
    """
    solver = 'sprayFoam'
    logFile = foamCase  + '/' + solver + '.log'
    patchNames = initializeParticlePositions(logFile, noPatches)
    patchTypes = ['none']*noPatches

    f = open(logFile)
    data = f.readlines()
    f.close()
    
    
    escapeParticles = np.array([getParticlesFromLog(line) for line in data if '- escape' in line])
    stickParticles = np.array([getParticlesFromLog(line) for line in data if '- stick' in line])
    totParticles = np.array([getParticlesFromLog(line) for line in data if '- parcels added' in line])
    currParticles = np.array([getParticlesFromLog(line) for line in data if 'Current number of parcels' in line])
    
    particles = np.zeros([len(stickParticles)/noPatches, noPatches+2])
    particles[:,noPatches+1] = totParticles
    particles[:,noPatches] = currParticles
    
    
    for i in range(noPatches):
        escapeArray = escapeParticles[i+1::noPatches+1]
        stickArray = stickParticles[i::noPatches]
        stickArray = np.append(0,stickArray[1:]-stickArray[:-1])
        particles[:,i] = escapeArray+stickArray
 
        if np.sum(escapeArray)>0:
            patchTypes[i]='escape'
        elif np.sum(stickArray)>0:
            patchTypes[i]='stick' 
#        
    if patchTypes.count('stick')==1:
        stickIndex = patchTypes.index('stick')
        escapeIndex = patchTypes.index('escape')
        print 'only one patch region: ' + patchNames[stickIndex] + ' with stick particles\nCorrecting for the openFOAM error...'
        
        particles[:, stickIndex] = particles [:, -1] - particles [:, -2] - particles[:, escapeIndex]
    return [patchNames, patchTypes, particles]
        

        
        
"""


Solving 2-D cloud sprayCloud
Cloud: sprayCloud
    Current number of parcels       = 70
    Current mass in system          = 4.717340119e-05
    Linear momentum                 = (1.927911278e-05 -0.0005505073982 -3.901855028e-07)
   |Linear momentum|                = 0.0005508450162
    Linear kinetic energy           = 0.006654607481
    Injector model1:
      - parcels added               = 106
      - mass introduced             = 7.17424883e-05
    Parcel fate: system (number, mass)
      - escape                      = 0, 0
    Parcel fate: patch (lowerWallInner|back|front|shieldInlet|nozzleInlet) (number, mass)
      - escape                      = 36, 2.45690871e-05
      - stick                       = 0, 0
    Parcel fate: patch (lowerWallOuter|outer) (number, mass)
      - escape                      = 0, 0
      - stick                       = 0, 0
    Parcel fate: patch (shield|upperWall|shieldOutlet) (number, mass)
      - escape                      = 0, 0
      - stick                       = 0, 0
    Temperature min/max             = 293, 293
    Mass transfer phase change      = 0
    D10, D32, Dmax (mu)             = 21.96959583, 26.54929668, 48.68546808
    Liquid penetration 95% mass (m) = 0.08693072042

"""