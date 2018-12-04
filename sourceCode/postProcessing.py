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
    This function evaluates the log file of the foamCase and gives the amount of particles in the 'scan' part of the log file. Default is the last part for speed. The number of regions distinguished in the sprayCloudProperties file must be specified using the 'noPatches' keyword.
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
    
    # VERY UGLY FUNCTION FOR NOW
    if scan=='last':         # get the last n lines of the logfile  
         n=200
         data = tailFile2(logFile, n)
         try:
             data = data[data.index('Solving 2-D cloud sprayCloud\n'):]
         except:
             try:
                 f = open(logFile)
             except:
                 f = open(foamCase + '/log')
             data = tailFile(logFile, 2000) #take a safe margin
             data = data[data.index('Solving 2-D cloud sprayCloud\n'):]
             f.close()
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

def getNearestIndex(array, value):
    array = np.array(array)
    return np.argmin(np.abs(array-value))
    
def getPeriodIndex(time, ydata, periodApprox=0.33, minOrMax='max'):
    """
    This function approaches the period of a signal over one period using a 
    (unstructured)-time array and signal.
    """
    timeIndex1  = 0;
    timeIndex2 = np.argmax(time>(time[0]+periodApprox))
    if minOrMax=='max':
        yIndex = np.argmax(ydata[timeIndex1:timeIndex2])
    else:
        yIndex = np.argmin(ydata[timeIndex1:timeIndex2])
    timeIndex = np.array([yIndex])
    timeY = np.array([time[yIndex]])

    i=0
    while timeY[i]+periodApprox<time[-1]:
        #   Approximate the minimum of the cycle to get a starting point for the next maximum  
        timeIndex1 = np.argmin(np.abs(time-(timeY[i]+periodApprox/2)))     #0.5 from maximum
        timeIndex2 = np.argmin(np.abs(time-(timeY[i]+3*periodApprox/2)))    #1.5 from maximum
        if timeIndex2==len(time):
            break
        if minOrMax=='max':
            yIndex = np.argmax(ydata[timeIndex1:timeIndex2]) + timeIndex1
        else:
            yIndex = np.argmin(ydata[timeIndex1:timeIndex2]) + timeIndex1
        timeIndex = np.append(timeIndex, yIndex)
        timeY = np.append(timeY, time[yIndex])
        i=i+1
    return timeIndex

def getPeriod(time, ydata, periodApprox=0.33, minOrMax='max'):
    """
    This function approaches the period of a signal over one period using a 
    (unstructured)-time array and signal.
    """
    timeIndex = getPeriodIndex(time, ydata, periodApprox=periodApprox, minOrMax='max')
    periods = time[timeIndex][1:]-time[timeIndex][:-1]
    print(periods)
    return np.average(periods)

def getPostProcessingFile(case, functionName):
    """
    This function returns the content of a postProcessing file in openfoam. 
    """
    filePath = case + "/postProcessing/"
    folders = os.listdir(filePath)
    for folder in folders:
        if functionName in folder:
            filePath = filePath + folder + "/"
            break
    print(filePath)
    filePath = filePath + os.listdir(filePath)[0] + "/"
    filePath = filePath + os.listdir(filePath)[0] 
    
    f = open(filePath)
    headerLines=0
    for line in f.readlines():
        if line.startswith("#"):
            headerLines+=1
        else:
            break
    f.close()    
    
    data = np.genfromtxt(filePath, skip_header=headerLines)
    time = data[:,0]
    keepRows= []
    for i in range(len(time)-1):
        if time[i]!=time[i+1]:
            keepRows.append(i)
    data = data[keepRows, :]
        
    return data

def getForceCoefficientIncompressible(case):
    data = getPostProcessingFile(case, "forceCoeffsIncompressible")
    forceCoeffs = {}
    forceCoeffs["time"] = data[:,0]
    forceCoeffs["cd"] = data[:,2]
    forceCoeffs["cl"] = data[:,3]
    return forceCoeffs


