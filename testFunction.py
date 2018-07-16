import os
os.sys.path.append('./sourceCode')
from writeFunctions import createOptimizeRunFile, createRunFile 
from foamFunctions import checkDicts
from foamFunctions import readInput

parameters = dict(B=1, bc=1,bs=1,ds=1,R=1,hsi=1,hso=1,hc=1,hio=1,F=1,angle=1)

foamCase = 'test'
parameterFile = 'parameters'
for parameter in parameters.keys():
    currentValue = readInput(parameterFile, parameter, foamCase)
    parameters[parameter]=currentValue

print parameters
#options 

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

options = dict(parallel=False, overwrite=True)


runFile = foamCase + '/Allrun.sh'
checkDicts(steps, foamCase)

createRunFile(runFile, steps, options)

# os.system(runFile)





