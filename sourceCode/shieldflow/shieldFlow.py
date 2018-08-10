# -*- coding: utf-8 -*-
"""
Functions to write instructions for openFOAM
"""
import os
import numpy as np
from foamFunctions import checkIfExist, getActiveDirs
import re

def checkIfShieldFlowCase(foamCase):
	"""
	Check if a certain foamCase exists
	"""
	nameSplit = foamCase.split('_')
	if len(nameSplit)==14:
	    return True
	else:
	    return False


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
	    try:
	        caseName = caseName + volumeParam + str(volumeParameters[volumeParam][0]) + '_'
	    except:
	        caseName = caseName + volumeParam + str(volumeParameters[volumeParam]) + '_'
	caseName = caseName[:-1]
	return caseName

def getParametersFromCase(foamCase):
	"""
	Get the parameters from the foamCase
	"""
	nP = 11
	parameters=dict()
	volumeParameters=dict()
	i=0
	if checkIfShieldFlowCase(foamCase):
		for P in foamCase.split('_'):
		    row = re.split('(\d.*)',P)
		    if i<nP:
		        try:
		            parameters[row[0]] = int(row[1])
		        except:
		            parameters[row[0]] = float(row[1])
		    else:
		        try:
		            volumeParameters[row[0]] = [int(row[1]), 0.1, 0.1]
		        except:
		            volumeParameters[row[0]] = [float(row[1]), 0.1, 0.1]    
		    i+=1
		return [parameters, volumeParameters]
	else:
		return 1
    
def findShieldCases(directory='.'):
    """
    Finds the corrupt cases in the current working directory or the specified folder.  0 means fine, 1 is running and 2 is unusable. don't work with relative paths.
    """
    if directory.endswith('/'):
        wd = directory
    elif len(directory)==1:
        wd = os.getcwd() + '/'
    else:
        wd = directory + '/'
    os.chdir(wd)
    
    caseDict = dict()
    cases = [elem for elem in os.listdir(wd) if os.path.isdir(wd + elem)]
    for case in cases:
        if checkIfShieldFlowCase(case):
            checkStatus = checkIfExist(case)
            # fix this bug in the checkstatus filed           
            if checkStatus==1:
                activeFoamCases = getActiveDirs('sprayFoam')
                if case in activeFoamCases:
                    caseDict[case]=1
                else:       # case is not running neither finished, so corrupt
                    caseDict[case]=2       
            else:       # case is fine
                caseDict[case]=0
            
    return caseDict


def cleanCorruptCases(directory='.'):
    """
    removes the corrupt shieldFlow folders from the specified directory. 
    """
    if directory.endswith('/'):
        wd = directory
    elif len(directory)==1:
        wd = os.getcwd() + '/'
    else:
        wd = directory + '/'
    os.chdir(wd)
    
    caseDict = findShieldCases(directory)
    for case in caseDict.keys():
        if caseDict[case]==1:
            print(case + ' is running')
        elif caseDict[case]==2:
            print(case + ' is corrupt, removed')
            os.system('rm -rf ' + case)  
    return