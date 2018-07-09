# -*- coding: utf-8 -*-
"""
Created on Sun Jul 01 18:05:33 2018

@author: Derek
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re

def getFoamFiles(foamCase, foamFolders=['system',  'constant', '0.orig']):
    """
    This case returns a list with all the files in which the openfoam data is present.
    Default folders to search are - system, constant and 0.orig folder.
    ADD SOME ERROR CHECKS
    """    
    foamFiles = []
    for foamFolder in foamFolders:
        casePath = foamCase + '/' + foamFolder + '/'
        results = [f for f in os.listdir(casePath)] # if os.path.isfile(f)]
        for result in results:
            path = casePath + result
            foamFiles.append(path)
    for foamFile in foamFiles:
        if os.path.isdir(foamFile):
            foamFiles.remove(foamFile)
    return foamFiles

def findFoamFile(foamCase, foamFile):
    """
    function to find the path of the file. Checks if the foamFile is a path or name
    """
    if len(foamFile.split('/'))==1:   
        foamFiles = getFoamFiles(foamCase)
        foamFilePath = [elem for elem in foamFiles if elem.endswith('/' + foamFile)][0]
    else:
        foamFilePath = foamFile
    return foamFilePath

def readInput(foamCase, foamFile, keyWord):
    """
    This function can find the corresponding entry for a certain keyword in an given openfoam case. 
    """
    foamFilePath = findFoamFile(foamCase, foamFile)

    f = open(foamFilePath)
    line = [string for string in f.readlines() if keyWord in string ]
    f.close()
    if line == []:
        return 0
    else:
        expr = keyWord+'\s*(.+?);'
        entry = re.search(expr, line[0]).group(1)
        return entry
    
def changeInput(foamCase, keyWord, newEntry, foamFile=None):
    """
    This function can find the corresponding entry for a certain keyword in an given openfoam case. 
    """
    foamFiles = getFoamFiles(foamCase)
    if foamFile==None:
        for fFile in foamFiles:
            entry = readInput(foamCase, fFile, keyWord)            
            if entry!=0:
                foamFile = fFile
                break
    else:
        entry = readInput(foamCase, foamFile, keyWord)
    
    if isinstance(entry, str):
        if entry==newEntry:
            print "For keyWord " + keyWord + " the entry " + entry + " does not change. No changes made"
        else:
            foamFilePath = findFoamFile(foamCase, foamFile)
            with open(foamFilePath, 'r') as f:
                fileData = f.read()
            fileData = fileData.replace(entry, newEntry)
            with open(foamFilePath, 'w') as f:
                f.write(fileData)
            print "keyWord " + keyWord + " changed entry from " + entry + " to " + newEntry + " in file " + foamFile
            f.close()
        return 0
    else:
        print "The keyWord: " + keyWord + " could not be found"
        return 0