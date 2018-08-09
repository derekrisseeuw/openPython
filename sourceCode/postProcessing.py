# -*- coding: utf-8 -*-
"""
File with functions to postprocess parts of openfoam
"""

import numpy as np
import os
import re
from foamFunctions import getTimeFolders
from foamFunctions import tailFile, tailFile2


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

    # initialize
    try:
        f = open(logFile)
    except:
        f = open(logFile.split('/')[0]+'/log')
        
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
          
def getParticlePositions(foamCase, noPatches, scan='last'):
    """
    This function evaluates the log file of the foamCase and gives the amount of particles that 
    """
    solver = 'sprayFoam'
    logFile = foamCase  + '/' + solver + '.log'
    patchNames = initializeParticlePositions(logFile, noPatches)
    patchTypes = ['none']*noPatches

    if os.path.isfile(logFile):
        logFile = logFile
    elif os.path.isfile(logFile.split('/')[0]+'/log'):
        logFile = logFile.split('/')[0]+'/log'
    else:
        print('logFile does not exist for case ' + foamCase)
        return
    
    if scan=='last':         # get the last n lines of the logfile 
         n=200
         data = tailFile2(logFile, n)
    else:
        try:
            f = open(logFile)
        except:
            f = open(foamCase + '/log')
        data = tailFile(logFile, n)
        f.close()
    
    # cut the data so it starts with a sprayCloud properties 
    data = data[data.index('Solving 2-D cloud sprayCloud\n'):]

    escapeParticles = np.array([getParticlesFromLog(line) for line in data if '- escape' in line])
    stickParticles = np.array([getParticlesFromLog(line) for line in data if '- stick' in line])
    totParticles = np.array([getParticlesFromLog(line) for line in data if '- parcels added' in line])
    currParticles = np.array([getParticlesFromLog(line) for line in data if 'Current number of parcels' in line])

    particles = np.zeros([int(len(stickParticles)/noPatches), noPatches+2])
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
        
    if patchTypes.count('stick')==1:
        stickIndex = patchTypes.index('stick')
        escapeIndex = patchTypes.index('escape')
        print('only one patch region: ' + patchNames[stickIndex] + ' with stick particles\nCorrecting for the openFOAM error...')
        
        particles[:, stickIndex] = particles [:, -1] - particles [:, -2] - particles[:, escapeIndex]
    return [patchNames, patchTypes, particles]
        
def goalFunction(particles):
    efficiency  = particles[0]/particles[-1]
    loss        = particles[1]/particles[-1]
    waste       = particles[2]/particles[-1]
    
    lossFactor = 100
    wasteFactor = 2
    goalValue = 100*        efficiency * \
                            np.exp(-lossFactor*loss) * \
                            (1-waste)**wasteFactor
    return goalValue