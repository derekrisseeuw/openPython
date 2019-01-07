import numpy as np
import matplotlib.pyplot as plt
import os

def readTurekReference(refCase):
    """
    Read the data from the reference cases and extract the time and displacement
    """
    name = "reference/ref_" + refCase.lower() + ".point" 
    data = np.genfromtxt(name)
    
    refData={}
    refData['time'] = data[:,0]
    refData['Ux'] = data[:,10]    
    refData['Uy'] = data[:,11]
    if refCase.lower() == "fsi1":
        refData['drag'] = data[:,6]    
        refData['lift'] = data[:,7]
    else:
        refData['drag'] = data[:,4] + data[:,6]    
        refData['lift'] = data[:,5] + data[:,7]
    return refData

def readCalculixGraph(case):
    """
    Read the graph files written by ccx and extract the time and displacement
    """
    files = ["graph_NA_DISP_D1.out", "graph_NA_DISP_D2.out"]
    graphData = {}
    for file in files:
        data = np.genfromtxt(case + "/" + file, skip_header=9)
        if "D1" in file:
            graphData['time'] = data[:,0]
            graphData['Ux'] = data[:,2]
        else:
            graphData['Uy'] = data[:,2]
    return graphData


def readOFgraph(case):
    """
    Read the graph files written by Openfoam and extract the time and displacement
    """
    file = "Adisplacement.log"
    f = open(case + "/" + file)
    lines = np.asarray((np.array([line.split('(')[1].split(')')[0].split() for line in f.readlines()])), float)
    f.close()
    keepLines = np.arange(2, len(lines), 2)
    lines = lines[keepLines, :]
    graphData={}
    graphData['Ux'] = lines[:,0]
    graphData['Uy'] = lines[:,1]
    return graphData


def readPointData(case):
    """
    Read all the pointdata files written by precice and extract the time and displacement
    """
    files = [ file for file in os.listdir(case) if file.startswith("point")]
    pointData = {}
    for file in files:
        dictName = file.split(".")[0]
        pointData[dictName]={}
        headers  = np.genfromtxt(case + "/" + file, max_rows=1, dtype=str)
        data = np.genfromtxt(case + "/" + file, skip_header=1)
        for i in range(len(headers)):
            header = headers[i]
            if header == 'Time':
                pointData[dictName]['time'] = data[:,i]
            elif header == "Displacements00":
                pointData[dictName]['Ux'] = data[:,i]
            elif header == "Displacements01":
                pointData[dictName]['Uy'] = data[:,i]
            elif header == "Displacements02":
                pointData[dictName]['Uz'] = data[:,i]
    return pointData

if __name__ == "__main__":
    case = "/home/derek/OpenFOAM/derek-v1712/run/FSI/FSI1/TUREK_FSI_UNIc"
    pointData = readPointData(case)
    plt.plot(pointData['point1']['time'], pointData['point1']['Ux'])
    plt.plot(pointData['point1']['time'], pointData['point1']['Uy'])

    
#        1	time
#5	drag on beam
#6	lift on beam
#7	drag on cylinder
#8	lift on cylinder
#11	Ux (x-displacement of point A)
#12	Uy (y-displacement of point A)