# -*- coding: utf-8 -*-
"""
file with fuctions to interact with openfoam 
"""

import numpy as np
import os
import re
from writeFunctions import Q2Vel, createOptimizeRunFile
#from time import sleep
from subprocess import check_output



def getSolverPIDs(solver):
    try:
        pids = check_output(['pgrep', solver]).decode("utf-8").split()
    except:
        pids=[]
    return pids

def checkNProcsBusy(solver='sprayFoam'):
    NProcsBusy = len(getSolverPIDs(solver))+len(getSolverPIDs('blockMesh'))
    return NProcsBusy


def getFoamFiles(foamCase='.', foamFolders=['system',  'constant', '0.orig']):
    """
    This case returns a list with all the files in which the openfoam data is present.
    Default folders to search are - system, constant and 0.orig folder.
    Default directory is the current working directory
    ADD SOME ERROR CHECKS
    """    
    foamFiles = []
    for foamFolder in foamFolders:
        casePath = foamCase + '/' + foamFolder + '/'
        if os.path.isdir(casePath):
            results = [f for f in os.listdir(casePath)] # if os.path.isfile(f)]
            for result in results:
                path = casePath + result
                foamFiles.append(path)
        else:
           print('The folder ' + foamFolder + ' does not exist. Moving on...\n')
 
    return foamFiles

def findFoamFile(foamFile, foamCase='.'):
    """
    function to find the path of the file. Checks if the foamFile is a path or name
    """
    if len(foamFile.split('/'))==1:   
        foamFiles = getFoamFiles(foamCase)
        foamFilePath = [elem for elem in foamFiles if elem.endswith('/' + foamFile)][0]
    else:
        foamFilePath = foamFile
    return foamFilePath

def readInput(foamFile, keyWord, foamCase='.'):
    """
    This function can find the corresponding entry for a certain keyword in an given openfoam case. 
    """
    foamFilePath = findFoamFile(foamFile, foamCase)

    f = open(foamFilePath)
    line = [string for string in f.readlines() if keyWord in string ]
    f.close()
    if line == []:
        return 0
    else:
        expr = '\A' + keyWord+'\s+(.+?);'
        for i in range(len(line)):
            try:
                entry = re.search(expr, line[i]).group(1)
            except:
                pass
        return entry
    
def changeInput(keyWord, newEntry, foamFile=None, foamCase='.'):
    """
    This function can find the corresponding entry for a certain keyword in an given openfoam case.
    Inputs are: (keyWord, newEntry, foamFile=None, , foamCase='.') 
    """
    newEntry = str(newEntry)
    foamFiles = getFoamFiles(foamCase)
    if foamFile==None:
        for fFile in foamFiles:
            entry = readInput(fFile, keyWord, foamCase)            
            if entry!=0:
                foamFile = fFile
                break
    else:
        entry = readInput(foamFile, keyWord, foamCase)
    
    if isinstance(entry, str):
        if entry==newEntry:
            print("For keyWord " + keyWord + " the entry " + entry + " does not change. No changes made")
        else:
            foamFilePath = findFoamFile(foamFile, foamCase)
            with open(foamFilePath, 'r') as f:
                fileData = f.read().split('\n')
            for i in range(len(fileData)):
                if (keyWord in fileData[i] and entry in fileData[i]):
                    fileData[i]=fileData[i].replace(entry, newEntry)
                    print(fileData[i])

            with open(foamFilePath, 'w') as f:
                f.write('\n'.join(fileData))
            print("keyWord " + keyWord + " changed entry from " + entry + " to " + newEntry + " in file " + foamFile)
            f.close()
        return 0
    else:
        print("The keyWord: " + keyWord + " could not be found")
        return 0

def checkDicts(steps, foamCase='.'):
    """
    This function checks whether the required dictionaries are defined in the openFOAM case. 
    input parameters are:
    (steps, foamCase='.')
    returns 1 if dictionary files lack. 
    """
    foamFiles  = getFoamFiles(foamCase)
    Files = [foamFile.split('/')[-1] for foamFile in foamFiles]
    result = 0
    exceptions = ['renumberMesh', 'prepare', 'checkMesh']
    for step in steps:
        if step=='run':
            dictFile = 'controlDict'
        elif step in exceptions:
            pass
        else: 
            dictFile = step + 'Dict'

        if dictFile not in Files:
            if any(step in file for file in Files):
                print("A dictionary file for " + step  + " is present, but has to be called with -dict option, take caution.")
            else:
                print("Cound not find " + dictFile + " in the openFOAM case " + foamCase)
                result = 1
    return result
    
def getTimeFolders(foamCase):
    timeFolders = []
    timeFoldersNum = []
    for file in os.listdir(foamCase):
        try:
            float(file)
            timeFolders.append(file)
            timeFoldersNum.append(float(file))
        except:
            pass
    sortArray = np.argsort(timeFoldersNum)
    timeFolders = np.array(timeFolders)
    timeFolders[sortArray]
    return timeFolders

def createCase(foamCase, baseCase):
    """
    Creates a new caseFolder based on the 'baseCase'. The shell script 'copyCase.sh' is used and assumed to be present.
    """
    if 'copyCase.sh' in os.listdir(baseCase):
        f = open('createNewCase.sh', 'w')
        writeLine = 'cd ' + baseCase + ' && ./copyCase.sh ' + foamCase 
        f.write(writeLine)
        f.close()
        os.system('./createNewCase.sh')
        os.remove(os.getcwd()+'/createNewCase.sh')
    else:
        print("ERROR. The script 'copyCase.sh' is not present in the baseCase directory. Please add this")
    return 0

def tailFile(logFile, n):
    """
    Returns the last n lines of a text file
    """
#    if os.path.isfile(logFile):
#        logFile = logFile
#    elif os.path.isfile(logFile.split('/')[0]+'/log'):
#        logFile = logFile.split('/')[0]+'/log'
    
    f = open(logFile)
    assert n>=0
    pos, lines = n+1, []
    while len(lines)<=n:
        try:
            f.seek(-pos,2)
            
        except IOError:
            f.seek(0)
            break
        finally:
            lines = list(f)
            pos *=2
    f.close()
    return lines[-n:]

def tailFile2(logFile, n):
    """
    A faster version of the tail file command
    """    
    try:
        tempFile = logFile + '.temp' 
        cmd1 = 'tail -n'+str(n) + ' ' +logFile + ' > ' + tempFile
        cmd2 = 'rm ' + tempFile
        os.system(cmd1)
        f = open(tempFile)
        lines = f.readlines()
        f.close()        
        os.system(cmd2)
    except:
        lines=[]
    return lines


def checkIfExist(foamCase):
    """ 
    Checks if a certain openfoam case exists. 0 is exists, 1 is running, 2 doesn't exist. 
    """
    if os.path.isdir(foamCase):
           endTime = readInput('controlDict', 'endTime', foamCase=foamCase)
           if os.path.isdir(foamCase+'/' + endTime):
               return 0
           else:
               return 1
    else:
        return 2
    
def returnProgress(foamCase):
    """
    Returns the progress of a case based on the time ran in percentage
    """
    status = checkIfExist(foamCase)
    if status==1:
        endTime = readInput('controlDict', 'endTime', foamCase=foamCase)
        logFile = foamCase + '/log'
        f = open(logFile)
        lines = tailFile(f, 100)
        f.close()
#        proc = subprocess.Popen(['tail', '-n100', logFile], stdout=subprocess.PIPE)
#        lines = proc.stdout.readlines()
        expr = '(?<=Time = ).*'
        for line in lines:
#            print('\n'+line)
#            'Time = ' in line
            if line.startswith('Time'):
                    Time = float(re.search(expr, line).group(0))
        progress = Time/float(endTime)*100
    elif status==0:
        progress = 100.
    elif status==2:
        progress = 0.
    return progress   
    
def runCase(foamCase, baseCase, parameters, volumeParameters, controlParameters, options=dict(parallel=False, overwrite=True)):
    """
    Takes all the input parameters, creates a new case and runs it. 
    returns 0: case has ran and is finished, 1: case has finished running by other application, 2 case is running
    """
    print('\n==============================================================\nRunning ' + foamCase + '\n==============================================================\n')
#                            
    status = checkIfExist(foamCase)
    if status != 2:
        print(foamCase + ' already exists. Continue with next case ...' )
        if status ==1:
            return 2  # for when the case is still running  
        else:
            return 1    # for when the case has finished running
    else:
        createCase(foamCase, baseCase)
            # get old parameters. 
        parameterFile = 'parameters'
        #for parameter in parameters.keys():
        #    currentValue = readInput(parameterFile, parameter, foamCase)
        #    parameters[parameter]=currentValue

#  Values to be changed
        print('\n\nChanging section\n\n\t\tGeometry')    
        for parameter in parameters.keys():
            changeInput(parameter, parameters[parameter], parameterFile, foamCase)

        print('\n\t\tVolumetric flow parameters')
        for volumeParameter in volumeParameters.keys():
            writeParameter = volumeParameter.replace('Q', 'U')
            if volumeParameter=='QNozzleIn':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2], angle = 5)
            elif volumeParameter=='QShieldIn':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2])
            elif volumeParameter=='QShieldOut':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2], direction=[0, 1, 0])
            print(velocity)
            changeInput(volumeParameter, volumeParameters[volumeParameter][0], parameterFile, foamCase)        # for visual interpretation in parameters file
            changeInput(writeParameter, velocity, 'U', foamCase)                  # for the inflow condition
            
        print('\n\t\tControl parameters ')
        for controlParameter in controlParameters.keys():
            changeInput(controlParameter, controlParameters[controlParameter], 'controlDict', foamCase)
        

        print('\n\t\tRunning section')
        #steps 
        steps =[
                    'blockMesh',
                    'extrudeMesh',
                    'changeDictionary',
                    'createPatch',
                    'renumberMesh',
                    'checkMesh',
                    'prepare',
                    'run',
        ]
        
        checkResult = checkDicts(steps, foamCase=foamCase)
        if checkResult==1:
            print('\n\t\tContinue to the next case... \n')
            return 2
        else:
            runFile = foamCase + '/Allrun.sh'
            createOptimizeRunFile(runFile, steps, options, parameters)
            print('\t\tRunning....')
            os.system(runFile)              # actually run the file
            print('\t\tFinished run....')
            return 0


def runCase2(foamCase, baseCase, parameters, volumeParameters, controlParameters, options=dict(parallel=False, overwrite=True)):
    """
    Takes all the input parameters, creates a new case and runs it. 
    Returns the PID the run
    """
#    print('\n==============================================================\nRunning ' + foamCase + '\n==============================================================\n')
#                            
    status = checkIfExist(foamCase)
    if status != 2:
#        print(foamCase + ' already exists. Continue with next case ...' )
        print('-')
        if status ==1:
            return []  # for when the case is still running  
        else:
            return []    # for when the case has finished running
    else:   
        print('\n==============================================================\nRunning ' + foamCase + '\n==============================================================\n')

        createCase(foamCase, baseCase)
            # get old parameters. 
        parameterFile = 'parameters'
        #for parameter in parameters.keys():
        #    currentValue = readInput(parameterFile, parameter, foamCase)
        #    parameters[parameter]=currentValue

#  Values to be changed
        print('\n\nChanging section\n\n\t\tGeometry')    
        for parameter in parameters.keys():
            changeInput(parameter, parameters[parameter], parameterFile, foamCase)

        print('\n\t\tVolumetric flow parameters')
        for volumeParameter in volumeParameters.keys():
            writeParameter = volumeParameter.replace('Q', 'U')
            if volumeParameter=='QNozzleIn':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2], angle = 5)
            elif volumeParameter=='QShieldIn':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2])
            elif volumeParameter=='QShieldOut':
                velocity = Q2Vel(volumeParameters[volumeParameter][0], volumeParameters[volumeParameter][1], volumeParameters[volumeParameter][2], direction=[0, 1, 0])
            print(velocity)
            changeInput(volumeParameter, volumeParameters[volumeParameter][0], parameterFile, foamCase)        # for visual interpretation in parameters file
            changeInput(writeParameter, velocity, 'U', foamCase)                  # for the inflow condition
            
        print('\n\t\tControl parameters ')
        for controlParameter in controlParameters.keys():
            changeInput(controlParameter, controlParameters[controlParameter], 'controlDict', foamCase)
        

        print('\n\t\tRunning section')
        #steps 
        steps =[
                    'blockMesh',
                    'extrudeMesh',
                    'changeDictionary',
                    'createPatch',
                    'renumberMesh',
                    'checkMesh',
                    'prepare',
                    'run',
        ]
        
        checkResult = checkDicts(steps, foamCase=foamCase)
        if checkResult==1:
            print('\n\t\tContinue to the next case... \n')
            return 2
        else:
            solver = readInput('controlDict', 'application' , foamCase=foamCase)
            oldPIDs = getSolverPIDs(solver)
            runFile = foamCase + '/Allrun.sh'
            createOptimizeRunFile(runFile, steps, options, parameters)
            print('\t\tRunning....')
            os.system(runFile + ' &')              # actually run the file
            newPIDs = getSolverPIDs(solver)
            PIDs = []
            for pid in newPIDs:
                if pid not in oldPIDs:
                    PIDs.append(pid)
            return PIDs





    

        