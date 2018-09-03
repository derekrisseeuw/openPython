# -*- coding: utf-8 -*-
"""
Functions to write instructions for openFOAM
"""
import os
os.sys.path.append('/media/qlayerspc/DATA/Linux/OpenFOAM/run/python/sourceCode')
import numpy as np
from foamFunctions import checkIfExist, getActiveDirs
import re
from postProcessing import getParticlePositions, goalFunction

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
    Finds the corrupt cases in the current working directory or the specified folder.  0 means fine, 1 is running, 2 is unusable, and 3 does not exist. don't work with relative paths!
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
            # fix this bug in the checkstatus file           
            if checkStatus==1:
                activeFoamCases = getActiveDirs('sprayFoam')
                if case in str(activeFoamCases):
                    caseDict[case]=1
                else:       # case is not running neither finished, so corrupt
                    caseDict[case]=2  
            elif checkStatus==2:        # Finished 
                caseDict[case]=3
            elif checkStatus==3:        # corrupt
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

def paramsToGenesettings(parameters, volumeParameters):
    # See parameter order in gene class
    paramsList = list(parameters.values())[:]
    paramsList = paramsList+ [elem[0] for elem in list(volumeParameters.values())[:]]
    gene_settings = [(paramsList[0],   True,    150,    150,    0),       # B
                     (paramsList[1],  False,      1,     20,    1),       # bc
                     (paramsList[2],  False,      1,      3,    1),       # bs
                     (paramsList[3],  False,     20,     80,   10),       # ds
                     (paramsList[4],   True,   6.25,   6.25,   0.),       # R
                     (paramsList[5],  False,     10,     70,    5),       # hsi
                     (paramsList[6],  False,     10,     70,    5),       # hso
                     (paramsList[7],  False,     50,    100,   10),       # hc 
                     (paramsList[8],   True,     20,     20,    0),       # hio
                     (paramsList[9],   True,    0.7,    0.7,   0.),       # F
                     (paramsList[10],  True,      5,      5,    0),       # angle
                     (paramsList[11],  True,    150,    150,    0),       # QNozzleIn 
                     (paramsList[12], False,      0,   1000,  100),       # QShieldIn
                     (paramsList[13], False,      0,   1000,  100),       # QShieldOut                 
                     ]
    return gene_settings

def paramsListToGenesettings(paramsList):
    # See parameter order in gene class
    gene_settings = [(int(paramsList[0]),   True,    150,    150,    0),       # B
                     (int(paramsList[1]),  False,      1,     20,    1),       # bc
                     (int(paramsList[2]),  False,      1,      3,    1),       # bs
                     (int(paramsList[3]),  False,     20,     80,   10),       # ds
                     (paramsList[4],   True,   6.25,   6.25,   0.),       # R
                     (int(paramsList[5]),  False,     10,     70,    5),       # hsi
                     (int(paramsList[6]),  False,     10,     70,    5),       # hso
                     (int(paramsList[7]),  False,     50,    100,   10),       # hc 
                     (int(paramsList[8]),   True,     20,     20,    0),       # hio
                     (paramsList[9],   True,    0.7,    0.7,   0.),       # F
                     (int(paramsList[10]),  True,      5,      5,    0),       # angle
                     (int(paramsList[11]),  True,    150,    150,    0),       # QNozzleIn 
                     (int(paramsList[12]), False,      0,   1000,  100),       # QShieldIn
                     (int(paramsList[13]), False,      0,   1000,  100),       # QShieldOut                 
                     ]
    return gene_settings



def getShieldCaseResults(directory='.'):
    os.chdir(directory)
    
    ####--------------  Find the existing cases in the folder   -----------------------------####
    caseDict = findShieldCases(directory)
    #
    Nruns = len(caseDict)
    Nparams = 1 + len(list(caseDict.keys())[0].split('_'))
    results=dict()
    
    ####--------------  Load the previously found cases    ----------------------------------####
    writeFile = os.getcwd() + '/goalResults.dat'
    if os.path.isfile(writeFile):
        f = open(writeFile)
        for line in f.readlines():
            [foamCase, value] = line.split()
            results[foamCase] = float(value)
        f.close()
    
    ####--------------  Find the goal functions of the missing cases ------------------------####
    f = open(writeFile, 'a')
    for foamCase in caseDict.keys():
        if caseDict[foamCase]>0:
            print('case ' + foamCase + ' is ignored because it is still running or corrupt')
        elif (os.path.isdir(foamCase) and foamCase not in results.keys()):
            [patchNames, patchType, particles] =  getParticlePositions(foamCase, 3, scan='last')
            goalValue = goalFunction(particles[-1])
            line = foamCase +  ' ' + str(goalValue) + '\n'
            f.write(line)
            results[foamCase] = goalValue
    f.close()
    
    
    Nruns = len(results)
    i=0
    resultArray = np.zeros([Nruns, Nparams])
    for foamCase in results.keys():
        [params1, params2] =  getParametersFromCase(foamCase)
        resultArray[i, 0:len(params1)] = list(params1.values())
        resultArray[i, len(params1):-1] = [elem[0] for elem in list(params2.values())]
        resultArray[i,-1] = results[foamCase]
        i+=1    
    return resultArray