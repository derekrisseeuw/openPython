# -*- coding: utf-8 -*-
"""
Functions to write instructions for openFOAM
"""
import numpy as np

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

def Q2Vel(Q, ri, ro, angle=0, direction=[0, -1, 0], returnType='stringVector'):
    """ 
    This function takes the volumetric inflow and transforms it to an average velocity inflow. 
    The angle is optional, A stringVector or valueVector can be returned. 
    """
    direction= direction/np.linalg.norm(direction)          # normalize the direction vector
    direction[0] = np.sin(np.deg2rad(angle)) 
    area = np.pi*(float(ro)**2 - float(ri)**2)
    
    Umag = (Q/60000)/area
    velocity = direction*Umag
    
    if returnType=='stringVector':
        velocity = 'uniform ( ' + str(velocity[0]) + ' ' + str(velocity[1]) + ' ' + str(velocity[2]) + ' )' 
        return velocity
    elif returnType=='valueVector':
        return velocity
    else:
        print('Give valid returnType.')
        return 1
    
def createName(parameters, volumeParameters):
    """  
    Create an unique name for the runcase
    """
    caseName = ''
    for param in parameters.keys():
        caseName = caseName + param + str(parameters[param]) + '_'
    for volumeParam in volumeParameters.keys():
        caseName = caseName + volumeParam + str(volumeParameters[volumeParam][0]) + '_'
    caseName = caseName[:-1]
    return caseName