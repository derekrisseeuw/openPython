# -*- coding: utf-8 -*-
"""
Functions to write instructions for openFOAM
"""
import numpy as np
import re

def writeLog(utility):
    """
    This function moves the log file created by the foamJob command to the respective utility log file. 
    """
    logCommand = 'mv log ' + utility + '.log\n' 
    return logCommand
    
def writeOptimizeBlock(hsi, hso, f):
    """
    This function is customized to work with the blockmesh procedure of the wedge optimization procedure. 
    """
    if hsi>hso:
        blockFile = 'blockMeshDict1'
    elif hsi<hso:
        blockFile = 'blockMeshDict2'
    elif hsi==hso:
        blockFile = 'blockMeshDict3'
    writeCommand = 'foamJob -w blockMesh -dict system/' + blockFile + '\n'
    logCommand = writeLog('blockMesh')
    f.write(writeCommand)
    f.write(logCommand)
    
def initialize(f):
    """
    initializes the runfile to source the openFOAM runfunctions. 
    """
    string = 'cd ${0%/*} || exit 1    		 # Run from this directory\n. $WM_PROJECT_DIR/bin/tools/RunFunctions\n\n'
    f.write(string)
    return

def writeOverwrite(f, step, overWrite=True):
    """
    This function writes any parts for which the overwrite option is an option. Default is true . 
    """
    if overWrite==True:
        writeCommand = 'foamJob -w ' + step + ' -overwrite\n'
    else:
        writeCommand = 'foamJob -w ' + step + '\n'
        
    logCommand = writeLog(step)
    f.write(writeCommand)
    f.write(logCommand)

def writeApplication(f, parallel=False):
    """
    This function writes the the application for either serial or parallel cases. 
    """
    getAppString = 'solver=$(getApplication)	# Requires the application specified in controlDict\n'
    
    f.write(getAppString)
    if parallel:
        decomposeCommand = 'foamJob -w decomposePar -force\n'
        logCommand = writeLog('decomposePar')
        f.write(decomposeCommand)
        f.write(logCommand)
        f.write('\n\n')
        writeSolverCommand = 'foamJob -w -p $solver\n'
    else:
        writeSolverCommand = 'foamJob -w $solver\n'

    logCommand = writeLog('$solver')
    f.write(writeSolverCommand)
    f.write(logCommand)
    if parallel:
        reconstructCommand = 'foamJob -w reconstructPar\n'
        logCommand = writeLog('reconstrucPar')
        f.write(reconstructCommand)
        f.write(logCommand)
    return

def writePreparationRun(f, prepFile):
    """
    Function to write a line to run the meshing and preparing part of the run
    """
    writeString = '\n./' + prepFile.split('/')[-1] + '\n\n'
    f.write(writeString)
    return

def createOptimizeRunFile(runFile, steps, options=dict(parallel=False, overwrite=True), parameters={}):
    """
    This function creates a runfile for the optimization cases. Special is the blockmesh. 
    """
    prepFile = runFile + '.pre'
    f = open(prepFile,'w')
    initialize(f)
    for step in steps:
        if step=='blockMesh':
            writeOptimizeBlock(parameters['hsi'], parameters['hso'], f)
        elif step=='run':
            g = open(runFile, 'w')
            initialize(g)
            writePreparationRun(g, prepFile)
            writeApplication(g, options['parallel'])
            g.close()
        elif step=='prepare':
            f.write('restore0Dir\n')
        elif step in ['createPatch', 'renumberMesh']:  
            writeOverwrite(f, step, options['overwrite'])
        else:
            writeCommand = 'foamJob -w ' + step + '\n'
            logCommand = writeLog(step)        
            f.write(writeCommand)
            f.write(logCommand)
        f.write('\n')
    f.close()
    return

def createRunFile(runFile, steps, options=dict(parallel=False, overwrite=True)):
    """
    This function creates a runfile for any case based on a list with 
    steps which should be provided in the correct order.
    Optional are the parallel run, and mesh overwrite, which can be triggered via the 
    dictionary:  options=dict(parallel=False, overwrite=True)
    """
    prepFile = runFile + '.pre'
    f = open(prepFile,'w')
    initialize(f) 

    for step in steps:
        if step=='run':
            g = open(runFile, 'w')
            initialize(g)
            writePreparationRun(g, prepFile)
            writeApplication(g, options['parallel'])
            g.close()
        elif step=='prepare':
            f.write('restore0Dir\n')
        elif step in ['createPatch', 'renumberMesh']:  
            writeOverwrite(f, step, options['overwrite'])
        else:
            writeCommand = 'foamJob -w ' + step + '\n'
            logCommand = writeLog(step)        
            f.write(writeCommand)
            f.write(logCommand)
        f.write('\n')
    f.close()
    return

def write6DoF(time, coors, angles, DoFFile='constant/6DoF.dat'):
    """
    Use this function to create a data file with coordinates and angles which openFOAM can read using the 6DoF reader
    """
    f = open(DoFFile, 'w')
    N = len(time)
    if N==len(coors) and N==len(angles):
        f.write('\n'+str(N) + '\n(\n')
        for i in range(N):
            string = '('+ str(time[i]) + ' ((' + str(coors[i,0]) + ' ' + str(coors[i,1]) + ' ' + str(coors[i,2]) + ') (' + str(angles[i,0]) + ' ' + str(angles[i,1]) + ' ' + str(angles[i,2]) + ')))\n'   
            f.write(string)
        f.write(')\n')
        f.close()
    else:
        print('The length of the arrays is not the same. Check the input.')

    return 0

