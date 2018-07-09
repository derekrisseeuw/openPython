import os
from subprocess import call

os.sys.path.append('./sourceCode')

from functions import *

foamCase = 'test'
foamFile = 'controlDict'
keyWord = 'writeInterval'
newEntry='1.0'

foamFiles = getFoamFiles(foamCase)
entry = readInput(foamCase, foamFile, keyWord)

changeInput(foamCase, keyWord, newEntry)



openFolder = "cd " + os.getcwd() + '/test'
#print os.popen('./testfile.sh').read()
import sys
os.system('./testFile.sh')