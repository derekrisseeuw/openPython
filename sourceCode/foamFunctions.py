# -*- coding: utf-8 -*-
"""
file with fuctions to interact with openfoam 
"""

import numpy as np
import os
import re

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
           print 'The folder ' + foamFolder + ' does not exist. Moving on...\n'
 
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
            print "For keyWord " + keyWord + " the entry " + entry + " does not change. No changes made"
        else:
            foamFilePath = findFoamFile(foamFile, foamCase)
            with open(foamFilePath, 'r') as f:
                fileData = f.read().split('\n')
            for i in range(len(fileData)):
                if keyWord in fileData[i]:
                    fileData[i]=fileData[i].replace(entry, newEntry)
                    print fileData[i]

            with open(foamFilePath, 'w') as f:
                f.write('\n'.join(fileData))
            print "keyWord " + keyWord + " changed entry from " + entry + " to " + newEntry + " in file " + foamFile
            f.close()
        return 0
    else:
        print "The keyWord: " + keyWord + " could not be found"
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
            print "Cound not find " + dictFile + " in the openFOAM case " + foamCase
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
        writeLine = 'cd ' + baseCase + '&& ./copyCase.sh ' + foamCase 
        f.write(writeLine)
        f.close()
        os.system('./createNewCase.sh')
        os.remove(os.getcwd()+'/createNewCase.sh')
    else:
        print "ERROR. The script 'copyCase.sh' is not present in the baseCase directory. Please add this"
    return 0
    