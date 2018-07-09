import numpy as np
import matplotlib.pyplot as plt
import os

## Collect the timeFolders
pwd = os.getcwd()
timeFolders = []
coordinateFiles = []
diameterFiles = []
massFiles = []
for fileName in os.listdir(pwd):
    try:
        float(fileName)
        timeFolders.append(fileName)
        coordinateFiles.append(pwd + '/' + fileName + '/lagrangian/sprayCloud/positions')
        diameterFiles.append(pwd + '/' + fileName + '/lagrangian/sprayCloud/d')
        massFiles.append(pwd + '/' + fileName + '/lagrangian/sprayCloud/mass0')
    except:
        pass

## Collect the data from the files
dtypes= [('x', '<f8'), ('y', '<f8'), ('z', '<f8'), ('a', '<i8')]
#dtypes= [float, float, float, int]
converterfunc1 = lambda x: float(x.strip("("))
converterfunc2 = lambda x: float(x.strip(")"))
#delim= ('(, ))
time = np.zeros([len(timeFolders),1])
dataDiam=np.empty([])
y = np.empty([])

startTime = 200;
for i in range(len(timeFolders)-2,len(timeFolders)-1):
    time[i] = float(timeFolders[i])
    try:
        dataCoor = np.genfromtxt(coordinateFiles[i], skip_header=19, skip_footer=4, converters={0:converterfunc1, 2:converterfunc2})
        x = dataCoor[:,0]
        y = dataCoor[:,1]
        z = dataCoor[:,2]
    except:
        pass 

dataDiam = np.genfromtxt(diameterFiles[i], skip_header=20, skip_footer=4)
d = dataDiam*1.e6
dataMass = np.genfromtxt(massFiles[i], skip_header=20, skip_footer=4)
m = dataMass

# validate the mass of the particles by comparing to the real mass
dataVolume = np.pi*dataDiam**3/6.        # m3 per particle
rho = 1620.                             # kg/m3
valMass = rho*dataVolume

NP = len(d)

## plot the figures 
#plt.figure(1)
#plt.plot(d, y, 'p', label='openFOAM case')
#plt.title('Particle stopping distance')
#plt.xlabel('particle Diameter (um)')
#plt.ylabel('travel distance (m)')
#plt.legend(loc=0)

plt.figure(2)
plt.plot(d, m,'p')
plt.plot(d, valMass)
plt.title('Particle mass vs diameter')
plt.xlabel('particle Diameter (um)')
plt.ylabel('particle mass (kg)')



#plt.figure(2)
#plt.plot(x, z,'p')
#plt.axis('equal')
#plt.title('Particle injection shape')
#plt.xlabel('x-position injection (m)')
#plt.ylabel('y-position injection (m)')
##
plt.figure(3)
plt.hist(d, int(NP/100. + 1))#plt.plot()
plt.title('Particle distribution')
plt.xlabel('particle diameter (um)')
plt.ylabel('probability')

print 'Total number of particles is '+ str(NP)

plt.show()
