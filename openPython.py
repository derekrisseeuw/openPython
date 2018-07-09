import os

os.sys.path.append('./sourceCode')

from functions import *

foamCase = 'test'
foamFile = 'controlDict'
keyWord = 'extrudeModel'
newEntry='linearNormal'

foamFiles = getFoamFiles(foamCase)
entry = readInput(foamCase, foamFile, keyWord)

changeInput(foamCase, keyWord, newEntry)


