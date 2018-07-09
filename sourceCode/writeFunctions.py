# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:49:40 2018

@author: qlayerspc
"""

def writeLog(utility):
    logCommand = 'mv log ' + utility + '.log\n' 
    return logCommand
    
    
def writeBlock(hsi, hso, f):
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
    string = 'cd ${0%/*} || exit 1    		 # Run from this directory\n. $WM_PROJECT_DIR/bin/tools/RunFunctions\n\n'
    f.write(string)
    return

def writeOverwrite(f, step, overWrite=True):
    if overWrite==True:
        writeCommand = 'foamJob -w ' + step + ' -overwrite\n'
    else:
        writeCommand = 'foamJob -w ' + step + '\n'
        
    logCommand = writeLog('blockMesh')
    f.write(writeCommand)
    f.write(logCommand)

def writeApplication(f, parallel=False):
    getAppString = 'solver=$(getApplication)	# Requires the application specified in controlDict\n'
    
    f.write(getAppString)
    if parallel:
        decomposeCommand = 'foamJob -w decomposePar\n'
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

def createRunFile(runFile, steps, options=dict(parallel=False, overwrite=True), parameters={}):
    f = open(runFile, 'w')
    initialize(f)
    for step in steps:
        if step=='blockMesh':
            writeBlock(parameters['hsi'], parameters['hso'], f)
        elif step=='run':
            writeApplication(f, options['parallel'])
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
        



    
    