"""
Subroutines for OpenFOAM integration.
"""

#===============================================================================
# S U B R O U T I N E S
#===============================================================================
import numpy as np
import csv as csv
import scipy.interpolate as interp
from scipy.interpolate import griddata
from scipy import spatial
import os
import subprocess

def read_RANS_data(case_dir, nx_RANS, ny_RANS, endTime, cart_interp=False, meshRANS=None):
    """
    Read data from RANS OpenFOAM case and store it in a dictionary.

    Parameters
    ----------
    case_dir : string
        Directory to read data from.
    nx_RANS, ny_RANS : integer
        Number of divisions in RANS mesh.
    endTime : integer or float
        Iteration to read data from.
    turb_model : string
        Turbulent model used.
    cart_interp : bool, optional
        Perform Cartesian interpolation of variables.
    meshRANS : ndarray, optional
        RANS mesh in the format output in read_RANS_mesh.
        Compulsory if cart_interp==True.

    Returns
    -------

    See Also
    --------
    read_RANS_mesh : Read RANS mesh from OpenFOAM case.

    """
    # Dictionary to store variables.
    data_RANS = {}
    # Obtain RANS mesh if it not given as input.
    if meshRANS==None:
        data_RANS['mesh'] = \
            read_RANS_mesh(case_dir, nx_RANS, ny_RANS, endTime, read_cell_surface=False)
    else:
        data_RANS['mesh'] = meshRANS
    # Obtain variables.
    U_RANSlist  = getRANSVector(case_dir, endTime, 'U')
    U_RANS      = getRANSPlane(U_RANSlist, '2D', nx_RANS, ny_RANS, 'vector')
    p_RANSlist  = getRANSScalar(case_dir, endTime, 'p')
    p_RANS      = getRANSPlane(p_RANSlist, '2D', nx_RANS, ny_RANS, 'scalar')
    data_RANS['um'] = U_RANS[0]
    data_RANS['vm'] = U_RANS[1]
    data_RANS['wm'] = U_RANS[2]
    data_RANS['pm'] = p_RANS[0]
    try:
        tau_momlist = getRANSSymmTensor(case_dir, endTime,
                                       'turbulenceProperties:R')
        tau_mom     = getRANSPlane(tau_momlist, '2D',
                                   nx_RANS, ny_RANS, 'tensor')
        data_RANS['uu'] = tau_mom[0][0]
        data_RANS['vv'] = tau_mom[1][1]
        data_RANS['ww'] = tau_mom[2][2]
        data_RANS['uv'] = tau_mom[0][1]
        data_RANS['k'] = 1./2.*(data_RANS['uu']+data_RANS['vv']+data_RANS['ww'])
    except:
        print("Reynolds stress tensor not found!")
    # Additional variables are read if they exist.
    try:
        vortlist    = getRANSVector(case_dir, endTime, 'vorticity')
        vort        = getRANSPlane(vortlist, '2D', nx_RANS, ny_RANS, 'vector')
        data_RANS['vorx'] = vort[0]
        data_RANS['vory'] = vort[1]
        data_RANS['vorz'] = vort[2]
    except:
        print("Vorticity not found!")
    try:
        Qlist       = getRANSScalar(case_dir, endTime, 'Q')
        Q           = getRANSPlane(Qlist, '2D', nx_RANS, ny_RANS, 'scalar')
        data_RANS['Q'] = Q[0]
    except:
        print("Q not found!")

    # Perform interpolation in Cartesian mesh.
    variables = ['um', 'vm', 'wm', 'pm', 'uu', 'vv', 'ww', 'uv', 'k']
    if cart_interp:
        data_RANS = interp_data_cart_RANS(data_RANS['mesh'], nx_RANS, ny_RANS,
                                          data_RANS, variables,
                                          dx_cart=0.1, dy_cart=0.001,
                                          nan_to_num=False)
    # Return data.
    return data_RANS

def getRANSfileName(case,time,var):
    fileName = case + '/' + str(time) + '/' + var
    if os.path.isfile(fileName):
        return fileName
    else:
        found=False
        i=10
        while (not found and i<30):
            line =  case + "/%." + "%if" % (i)
            line2 = '/' + var
            line = line % time
            fileName = line + line2
            if os.path.isfile(fileName):
                return fileName
                found=True
            else:
                i+=1
            
        if found==False:
            fileName = case + '/' + str(int(time)) + '/' + var
            if os.path.isfile(fileName):
                return(fileName)

def getRANSfile(case,time,var):
    try:
        file = open(case + '/' + str(time) + '/' + var,'r').readlines()
        return file
    except:
        i=14
        found=False
        while (not found and i<30):
            try:
                line =  case + "/%." + "%if" % (i)
                line2 = '/' + var
                line = line % time
                varName = line + line2
                file = open(varName, 'r').readlines()
                found=True
                return file
            except:
                i+=1
                #break to avoid infinite loop 
        if found==False:
            file = open(case + '/' + str(int(time)) + '/' + var,'r').readlines()
            return file

def getRANSScalar(case, time, var):
    file = getRANSfile(case, time, var)

#    file = open(case + '/' + str(time) + '/' + var,'r').readlines()
    #lines=0
    tmp = []
    tmp2 = 10**12
    maxIter = -1
    #v= np.zeros([3,70000])
    #cc = False
    j = 0
    for i,line in enumerate(file):
        if 'internalField' in line:
            tmp = i + 1
            tmp2 = i + 3
            #cc = True
            #print(tmp, tmp2)
        elif i==tmp:
            maxLines = int(line.split()[0])
            maxIter  = tmp2 + maxLines
            v = np.zeros([1,maxLines])
            ##print(maxLines, maxIter)
        elif i>=tmp2 and i<maxIter:
            #tmp3=i
            linei = line.split()
            #v[:,j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2].split(')')[0])]
            v[:,j] = [float(linei[0])]
            j += 1
    return v

def getRANSVector(case, time, var):
    file = getRANSfile(case,time,var)
    #lines=0
    tmp = []
    tmp2 = 10**12
    maxIter = -1
    #v= np.zeros([3,70000])
    #cc = False
    j = 0
    for i,line in enumerate(file):
        if 'internalField' in line:
            tmp = i + 1
            tmp2 = i + 3
            #cc = True
            ##print(tmp, tmp2)
        elif i==tmp:
            maxLines = int(line.split()[0])
            maxIter  = tmp2 + maxLines
            v = np.zeros([3,maxLines])
           # #print(maxLines, maxIter)
        elif i>=tmp2 and i<maxIter:
            linei = line.split()
            v[:,j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2].split(')')[0])]
            j += 1
    return v

def getRANSTensor(case, time, var):
    file = getRANSfile(case,time,var)
#    file = open(case + '/' + str(time) + '/' + var,'r').readlines()
    #file = open('wavyWall_Re6850_komegaSST_4L_2D/20000/gradU','r').readlines()
    #lines=0
    tmp = []
    tmp2 = 10**12
    maxIter = -1
    #v= np.zeros([3,70000])
    #cc = False
    j = 0
    for i,line in enumerate(file):
        if 'internalField' in line:
            tmp = i + 1
            tmp2 = i + 3
            #cc = True
            #print(tmp, tmp2)
        elif i==tmp:
            maxLines = int(line.split()[0])
            maxIter  = tmp2 + maxLines
            v = np.zeros([3,3,maxLines])
            #print(maxLines, maxIter)
        elif i>=tmp2 and i<maxIter:
            #tmp3=i
            linei = line.split()
            v[0,:,j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2])]
            v[1,:,j] = [float(linei[3]), float(linei[4]), float(linei[5])]
            v[2,:,j] = [float(linei[6]), float(linei[7]), float(linei[8].split(')')[0])]

            j += 1

    return v

def getRANSSymmTensor(case, time, var):
    file = getRANSfile(case,time,var)
#    file = open(case + '/' + str(time) + '/' + var,'r').readlines()
    #file = open('wavyWall_Re6850_komegaSST_4L_2D/20000/gradU','r').readlines()
    #lines=0
    tmp = []
    tmp2 = 10**12
    maxIter = -1
    #v= np.zeros([3,70000])
    #cc = False
    j = 0
    for i,line in enumerate(file):
        if 'internalField' in line:
            tmp = i + 1
            tmp2 = i + 3
            #cc = True
            #print(tmp, tmp2)
        elif i==tmp:
            maxLines = int(line.split()[0])
            maxIter  = tmp2 + maxLines
            v = np.zeros([3,3,maxLines])
            #print(maxLines, maxIter)
        elif i>=tmp2 and i<maxIter:
            #tmp3=i
            linei = line.split()
            v[0,:,j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2])]
            v[1,:,j] = [float(linei[1]), float(linei[3]), float(linei[4])]
            v[2,:,j] = [float(linei[2]), float(linei[4]), float(linei[5].split(')')[0])]

            j += 1

    return v

def getRANSPlane(mesh, dimension, nx, ny, t='vector',a='yesAve'):
    xRANS = np.zeros([nx,ny])
    yRANS = np.zeros([nx,ny])
    zRANS = np.zeros([nx,ny])
    #print(mesh.shape)

    if a=='yesAve':
        if t=='vector':
            if dimension=='3D':
                for i in range(ny):
                    print("3D")
            # xRANS[:,i] = mesh[0,i*256*128:256+i*256*128]
            # yRANS[:,i] = mesh[1,i*256*128:256+i*256*128]
            # zRANS[:,i] = mesh[2,i*256*128:256+i*256*128]
            elif dimension=='2D':
                for i in range(ny):
                    xRANS[:,i] = mesh[0,i*nx:nx+i*nx]
                    yRANS[:,i] = mesh[1,i*nx:nx+i*nx]
                    zRANS[:,i] = mesh[2,i*nx:nx+i*nx]

            return np.array([xRANS, yRANS, zRANS])

        elif t=='scalar':
            for i in range(ny):
                xRANS[:,i] = mesh[0,i*nx:nx+i*nx]

            return np.array([xRANS])

        elif t=='tensor':
            out = np.zeros([3,3,nx,ny])
            for i in range(ny):
                out[:,:,:,i] = mesh[:,:,i*nx:nx+i*nx]

            return out

    elif a=='noAve':
        if t=='vector':
            if dimension=='3D':
                for i in range(96):
                    xRANS[:,i] = mesh[0,i*256*128:256+i*256*128]
                    yRANS[:,i] = mesh[1,i*256*128:256+i*256*128]
                    zRANS[:,i] = mesh[2,i*256*128:256+i*256*128]
            elif dimension=='2D':
                for i in range(96):
                    xRANS[:,i] = mesh[0,i*256:256+i*256]
                    yRANS[:,i] = mesh[1,i*256:256+i*256]
                    zRANS[:,i] = mesh[2,i*256:256+i*256]

            return np.array([xRANS, yRANS, zRANS])

def getRANSField(mesh, dimension, nx, ny, nz, t='vector'):
    xRANS = np.zeros([nx,ny*2,nz])
    yRANS = np.zeros([nx,ny*2,nz])
    zRANS = np.zeros([nx,ny*2,nz])
    #print(mesh.shape)

    kk=0

    if t=='vector':
        if dimension=='3D':
            print("3D")
            for j in range(nz):
                for i in range(ny):
                    xRANS[:,i,j] = mesh[0,i*nx+nx*ny*(j+kk*4):nx+i*nx+nx*ny*(j+kk*4)]
                    yRANS[:,i,j] = mesh[1,i*nx+nx*ny*(j+kk*4):nx+i*nx+nx*ny*(j+kk*4)]
                    zRANS[:,i,j] = mesh[2,i*nx+nx*ny*(j+kk*4):nx+i*nx+nx*ny*(j+kk*4)]

        elif dimension=='2D':
            for i in range(ny):
                xRANS[:,i] = mesh[0,i*nx:nx+i*nx]
                yRANS[:,i] = mesh[1,i*nx:nx+i*nx]
                zRANS[:,i] = mesh[2,i*nx:nx+i*nx]

        return np.array([xRANS, yRANS, zRANS])

    elif t=='scalar':
        if dimension=='3D':
            for i in range(ny):
                for j in range(nz):
                    xRANS[:,i,j] = mesh[0,i*nx+nx*ny*j:nx+i*nx+nx*ny*j]
        elif dimension=='2D':
            for i in range(ny):
                xRANS[:,i] = mesh[0,i*nx:nx+i*nx]

        return np.array([xRANS])

    elif t=='tensor':
        out = np.zeros([3,3,nx,ny])
        for i in range(ny):
            out[:,:,:,i] = mesh[:,:,i*nx:nx+i*nx]

        return out

def calcEigenvalues_general(tau):
    if len(tau.shape)==3:
        l=tau.shape[2]
        eigVal = np.zeros([3,l])
        for i in range(l):
            a,b=np.linalg.eig(tau[:,:,i])
            eigVal[:,i]=sorted(a, reverse=True)

def calcEigenvalues(tau, k):

    if len(tau.shape)==3:
        l=tau.shape[2]

        tauAni = np.zeros([3,3,l])
        for i in range(l):
                tauAni[:,:,i] = tau[:,:,i]/(2.*k[i]) - np.diag([1/3.,1/3.,1/3.])

        eigVal = np.zeros([3,l])
        for i in range(l):
            a,b=np.linalg.eig(tauAni[:,:,i])
            eigVal[:,i]=sorted(a, reverse=True)


    elif len(tau.shape)==4:
        l=tau.shape[2]
        l2=tau.shape[3]
        #print(l,l2)
        tauAni = np.zeros([3,3,l,l2])
        for i in range(l):
            for j in range(l2):
                tauAni[:,:,i,j] = tau[:,:,i,j]/(2.*k[i,j]) - np.diag([1/3.,1/3.,1/3.])

        eigVal = np.zeros([3,l,l2])
        for i in range(l):
            for j in range(l2):
                a,b=np.linalg.eig(tauAni[:,:,i,j])
                eigVal[:,i,j]=sorted(a, reverse=True)


    return eigVal

def calcEigenvalues2(tau, k):

    if len(tau.shape)==3:
        l=tau.shape[2]

        tauAni = np.zeros([3,3,l])
        for i in range(l):
                tauAni[:,:,i] = tau[:,:,i]

        eigVal = np.zeros([3,l])
        for i in range(l):
            a,b=np.linalg.eig(tauAni[:,:,i])
            eigVal[:,i]=sorted(a, reverse=True)


    elif len(tau.shape)==4:
        l=tau.shape[2]
        l2=tau.shape[3]
        #print(l,l2)
        tauAni = np.zeros([3,3,l,l2])
        for i in range(l):
            for j in range(l2):
                tauAni[:,:,i,j] = tau[:,:,i,j]

        eigVal = np.zeros([3,l,l2])
        for i in range(l):
            for j in range(l2):
                a,b=np.linalg.eig(tauAni[:,:,i,j])
                eigVal[:,i,j]=sorted(a, reverse=True)


    return eigVal

def barycentricMap(eigVal):

    if len(eigVal.shape)==2:
        l=eigVal.shape[1]

        C1c = eigVal[0,:] - eigVal[1,:]
        C2c = 2*(eigVal[1,:] - eigVal[2,:])
        C3c = 3*eigVal[2,:] + 1
        Cc  = np.array([C1c, C2c, C3c])

        locX = np.zeros([l])
        locY = np.zeros([l])
        for i in range(l):
            locX[i] = Cc[0,i] + 0.5*Cc[2,i]
            locY[i] = np.sqrt(3)/2 * Cc[2,i]

    elif len(eigVal.shape)==3:
        l=eigVal.shape[1]
        l2=eigVal.shape[2]

        C1c = eigVal[0,:,:] - eigVal[1,:,:]
        C2c = 2*(eigVal[1,:,:] - eigVal[2,:,:])
        C3c = 3*eigVal[2,:,:] + 1
        Cc  = np.array([C1c, C2c, C3c])

        locX = np.zeros([l,l2])
        locY = np.zeros([l,l2])
        for i in range(l):
            for j in range(l2):
                locX[i,j] = Cc[0,i,j] + 0.5*Cc[2,i,j]
                locY[i,j] = np.sqrt(3)/2 * Cc[2,i,j]


    return np.array([locX, locY])

def calcFracAnisotropy(tau):
    if len(tau.shape)==3:
        l=tau.shape[2]

        eigVal = np.zeros([3,l])
        for i in range(l):
            a,b=np.linalg.eig(tau[:,:,i])
            eigVal[:,i]=sorted(a, reverse=True)
        #eigValMean = eigVal.mean(0)
        FA = np.zeros([l])
        for i in range(l):
            # FA[i] = np.sqrt(3/2.) * np.sqrt( (eigVal[0,i] - eigValMean[i])**2. + (eigVal[1,i] - eigValMean[i])**2. + (eigVal[2,i] - eigValMean[i])**2.) / np.sqrt(eigVal[0,i]**2. + eigVal[1,i]**2. + eigVal[2,i]**2.)
            # FA[i] = np.sqrt(1/2.) * np.sqrt( (eigVal[0,i] - eigVal[1,i])**2. + (eigVal[1,i] - eigVal[2,i])**2. + (eigVal[2,i] - eigVal[0,i])**2.) / np.sqrt(eigVal[0,i]**2. + eigVal[1,i]**2. + eigVal[2,i]**2.)
            FA[i] = np.sqrt(1/2.) * np.sqrt((eigVal[0,i] - eigVal[1,i])**2. + (eigVal[1,i] - eigVal[2,i])**2. + (eigVal[2,i] - eigVal[0,i])**2.) / np.sqrt(eigVal[0,i]**2. + eigVal[1,i]**2. + eigVal[2,i]**2.)


    elif len(tau.shape)==4:
        l=tau.shape[2]
        l2=tau.shape[3]
        #print(l,l2)

        eigVal = np.zeros([3,l,l2])
        for i in range(l):
            for j in range(l2):
                a,b=np.linalg.eig(tau[:,:,i,j])
                eigVal[:,i,j]=sorted(a, reverse=True)

        #print(l,l2)
        #eigValMean = eigVal.mean(0)
        FA = np.zeros([l,l2])
        for i in range(l):
            for j in range(l2):
                # FA[i,j] = np.sqrt(3/2.) * np.sqrt( (eigVal[0,i,j] - eigValMean[i,j])**2. + (eigVal[1,i,j] - eigValMean[i,j])**2. + (eigVal[2,i,j] - eigValMean[i,j])**2.) / np.sqrt(eigVal[0,i,j]**2. + eigVal[1,i,j]**2. + eigVal[2,i,j]**2.)
                FA[i,j] = np.sqrt(1/2.) * np.sqrt( (eigVal[0,i,j] - eigVal[1,i,j])**2. + (eigVal[2,i,j] - eigVal[1,i,j])**2. + (eigVal[2,i,j] - eigVal[0,i,j])**2.) / np.sqrt(eigVal[0,i,j]**2. + eigVal[1,i,j]**2. + eigVal[2,i,j]**2.)

    return FA

def calcInvariant(eigVal):
    if len(eigVal.shape)==2:
        l=eigVal.shape[1]

        II = np.zeros([l])
        III = np.zeros([l])
        for i in range(l):
            II[i] = 2.*(eigVal[0,i]**2. + eigVal[0,i] * eigVal[1,i] + eigVal[1,i]**2.)
            III[i] = -3*eigVal[0,i]*eigVal[1,i]*(eigVal[0,i] + eigVal[1,i])

    elif len(eigVal.shape)==3:
        l=eigVal.shape[1]
        l2=eigVal.shape[2]

        II = np.zeros([l,l2])
        III = np.zeros([l,l2])
        for i in range(l):
            for j in range(l2):
                II[i,j] = 2.*(eigVal[0,i,j]**2. + eigVal[0,i,j] * eigVal[1,i,j] + eigVal[1,i,j]**2.)
                III[i,j] = -3*eigVal[0,i,j]*eigVal[1,i,j]*(eigVal[0,i,j] + eigVal[1,i,j])

    return II,III

def calcInitialConditions(U, turbulenceIntensity, turbLengthScale, nu, d, D):

    k       = 1.5 * (U*turbulenceIntensity)**2.0
    epsilon = 0.16 * k**1.5 / turbLengthScale
    omega   = 1.8 * np.sqrt(k) / turbLengthScale
    #omega_farfield = U/D
    omega_wall = 10 * 6 * nu / (0.0705 * d**2)
    #omega_wall_wilcox = 6 / (0.0708 * yPlus_wilcox**2)
    nuTilda = np.sqrt(1.5)*U*turbulenceIntensity*turbLengthScale
    nuTilda_NASA = 3*nu
    nut_NASA = 3*nu*(3**3)/(3**3 + 7.1**3)
    Re      = U*D/nu
    tmp = {'k': k, 'epsilon': epsilon, 'omega': omega, 'nuTilda': nuTilda, 
           'omega_wall':omega_wall, 'Re':Re}    
    
    return tmp


def getRANSScalarBoundary(case, time, var, selected_wall):
    file = getRANSfile(case,time,var)
#    file = open(case + '/' + str(time) + '/' + var,'r').readlines()

    write_line = False
    start_writing_counter = 0
    v = []
    j = 0
    for i, line in enumerate(file):
        linei = line.split()
        try: # For empty lines.
            linecool = linei[0]
        except: # If there is an empty line, break the loop.
            continue

        if (linei[0] == selected_wall):
            write_line = True
            print("Selected wall is " + linei[0])

        if (write_line == True):
            try: # Defines the number of elements based on the OpenFOAM dimensions located in the actual file.
                int(linei[0])
                start_writing_counter = i
#                print("Getting closer, the number of nodes is " + str(linei[0]))
                v = np.zeros([1, int(str(linei[0]))])
                nodes_number = int(str(linei[0]))
            except:
                pass
        if (start_writing_counter>0 and i>=start_writing_counter+2):
            if (i>=start_writing_counter+2+nodes_number):
                break
#            print('nodes number: ' + str(nodes_number))
            v[:, j] =  [float(linei[0])]
            j += 1

    return v

def getRANSVectorBoundary(case, time, var, selected_wall):
    file = getRANSfile(case,time,var)
#    file = open(case + '/' + str(time) + '/' + var,'r').readlines()

    write_line = False
    start_writing_counter = 0
    v = []
    j = 0
    for i, line in enumerate(file):
        linei = line.split()
        try: # For empty lines.
            linecool = linei[0]
        except: # If there is an empty line, break the loop.
            continue

        if (linei[0] == selected_wall):
            write_line = True
            print("Selected wall is " + linei[0])

        if (write_line == True):
            try: # Defines the number of elements based on the OpenFOAM dimensions located in the actual file.
                float(linei[0])
                start_writing_counter = i
#                print("Getting closer, the number of nodes is " + str(linei[0]))
                v = np.zeros([3, int(str(linei[0]))])
                nodes_number = int(str(linei[0]))
            except:
                pass

        if (start_writing_counter>0 and i>=start_writing_counter+2):
            if (i>=start_writing_counter+2+nodes_number):
                break
#            print('nodes number: ' + str(nodes_number))
            v[:, j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2].split(')')[0])]
            j += 1

    return v

def loadData_avg(dataset, var_calc=False):
    if var_calc:
        data_list = np.zeros([8, 100000])
    else:
        data_list = np.zeros([10, 100000])
    with open(dataset, 'rb') as f:
        reader = csv.reader(f)
        names = reader.next()[:-1]
        for i, row in enumerate(reader):
            if row:
                data_list[:, i] = np.array([float(ii) for ii in row[:-1]])

    data_list = data_list[:, :i]

    data = {}
    for i, var in enumerate(names):
        data[var] = data_list[i, :]

    return data

def interpDNSOnRANS(dataDNS, meshRANS):
    names = dataDNS.keys()
    data = {}
    xy = np.array([dataDNS['x'], dataDNS['y']]).T
    for var in names:
        if not var == 'x' and not var == 'y':
            data[var] = interp.griddata(
                xy, dataDNS[var], (meshRANS[0, :, :], meshRANS[1, :, :]),
                method='linear')

    return data

def interpUnstructured(dataLaminar, plotMesh):
    names = dataLaminar.keys()
    data = {}
#    xy = np.array([data['mesh'][0],data['mesh'][1]]).T
    for var in names:
        if not var == 'mesh':
            data[var] = interp.griddata(
                (dataLaminar['mesh'][0].T[0], dataLaminar['mesh'][1].T[0]), 
                dataLaminar[var].T[0], 
                (plotMesh[0], plotMesh[1]), 
                method='linear')
            data[var] = np.nan_to_num(data[var])
    return data

def writeP(case, time, var, data):
    # file = open(case + '/' + str(time) + '/' + var,'r').readlines()
    copy(case + '/' + str(time) + '/' + var, case + '/' + str(time) + '/' + var)
    # file = open('R~','r+').readlines()
    # file = open('wavyWall_Re6850_komegaSST_4L_2D/20000/gradU','r').readlines()
    # lines=0
    tmp = []
    tmp2 = 10 ** 12
    maxIter = -1
    # v= np.zeros([3,70000])
    cc = False
    j = 0
    file_path = case + '/' + str(time) + '/' + var
    #print(file_path)
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as file:
            for i, line in enumerate(file):
                if 'object' in line:
                    new_file.write('    object      p;\n')
                elif cc == False and 'internalField' not in line:
                    new_file.write(line)

                elif 'internalField' in line:
                    tmp = i + 1
                    tmp2 = i + 3
                    cc = True
                    new_file.write(line)
                    #print(tmp, tmp2)


                elif i == tmp:
                    #print(line.split())
                    maxLines = int(line.split())
                    maxIter = tmp2 + maxLines
                    # v = np.zeros([3,3,maxLines])
                    new_file.write(line)
                    #print(maxLines, maxIter)

                elif i > tmp and i < tmp2:
                    new_file.write(line)

                elif i >= tmp2 and i < maxIter:
                    # print line
                    new_file.write(str(data[0, 0, j]) + '\n')
                    # tmp3=i
                    # print line
                    # file.write('fuck')
                    # line.replace(line, 'fuck')
                    # linei = line.split()
                    # v[0,:,j] = [float(linei[0].split('(')[1]), float(linei[1]), float(linei[2])]
                    # v[1,:,j] = [float(linei[3]), float(linei[4]), float(linei[5])]
                    # v[2,:,j] = [float(linei[6]), float(linei[7]), float(linei[8].split(')')[0])]

                    j += 1

                elif i >= maxIter:
                    new_file.write(line)

    fh.close()
    remove(file_path)
    move(abs_path, file_path)

    # return v

def read_RANS_mesh(case_dir, nx_RANS, ny_RANS, endTime, read_cell_surface=False):
    """
    Read RANS mesh from OpenFOAM case.

    Parameters
    ----------
    case_dir : string
        Case directory where the RANS mesh is located.
    nx_RANS, ny_RANS : float
        Number of divisions of RANS mesh.
    read_cell_surface : Bool, optional
        Additionally read and return cell surfaces.

    Returns
    -------
    meshRANS : ndarray
        RANS mesh in the format [i,j,k].
        i : x, y, z component.
        j : x-divisions.
        k : y-divisions.
    """
    meshRANSlist = np.zeros((3, nx_RANS*ny_RANS))
    meshRANSlist[0] = getRANSScalar(case_dir, endTime, 'Cx')
    meshRANSlist[1] = getRANSScalar(case_dir, endTime, 'Cy')
    meshRANSlist[2] = getRANSScalar(case_dir, endTime, 'Cz')
    meshRANS =        getRANSPlane(meshRANSlist, '2D', nx_RANS,
                                   ny_RANS, 'vector')

    if read_cell_surface:
        # Get cell volumes.
        mesh_cellsurface_RANS_list = getRANSScalar(case_dir, '0', 'V')
        mesh_cellsurface_RANS=getRANSPlane(mesh_cellsurface_RANS_list,'2D',
                                           nx_RANS, ny_RANS, 'scalar')
        return meshRANS, mesh_cellsurface_RANS
    else:
        return meshRANS

def interp_data_cart_RANS(meshRANS, nx_RANS, ny_RANS, data, variables, dx_cart=0.1, dy_cart=0.00001, nan_to_num=False):
    """Interpolate RANS data into a Cartesian mesh.

    Interpolate data from meshRANS, with nx_RANS and ny_RANS, to new mesh
    given by x_xgrid_list and y_grid_list.

    Values are stored in data[var_cart], with "data" being a dictionary.

    Parameters
    ----------
    meshRANS : numpy ndarray
        Original RANS mesh in 3D ndarray format.

    nx_RANS, ny_RANS : float
        Number of spacings in RANS data.

    data : dictionary
        Import and store values.

    variables : list
        List of strings of variables to interpolate.

    dx_cart, dy_cart : optional, int, float
        x and y divisions of the Cartesian interpolation.

    nan_to_num : optional, Boolean
        Convert nan values to zeros.

    Returns
     -------
    data : dictionary
        Old data with new variables x_cart, y_cart and um_cart.
    """

    x_grid_list = np.arange(0, 9.0+dx_cart, dx_cart)
    y_grid_list = np.arange(0, 3.036+dy_cart, dy_cart)

    data['x_cart'], data['y_cart'] = np.meshgrid(x_grid_list, y_grid_list)
    for var in variables:
        data[var+'_cart'] = griddata((
            np.swapaxes(meshRANS[0,:,:], 0, 1).reshape(nx_RANS * ny_RANS),
            np.swapaxes(meshRANS[1,:,:], 0, 1).reshape(nx_RANS * ny_RANS)),
            np.swapaxes(data[var], 0, 1).reshape(nx_RANS * ny_RANS),
            (data['x_cart'], data['y_cart']), method='linear')
        if nan_to_num:
            data[var+'_cart'] = np.nan_to_num(data[var+'_cart'])
    return data


def postprocessing_OpenFOAM(case_dir, solver, options=[]):
    """
    Perform post-processing operations for OpenFOAM case.

    pre_processing.bash file needed!!!

    Parameters
    ----------
    case_dir : string
        Directory of the OpenFOAM case.
    solver : string
        Solver name.

    Returns
    -------

    """
    # write the options
    os.chdir(case_dir)
    for option in options:    
        subprocess.call(solver
            + ' -postProcess -func ' + option + ' > ' + option + '.log',
              shell=True)

    # Write cell centres components.
    subprocess.call(solver
            + ' -postProcess -func writeCellCentres -time 0 > writeCellCentres.log',
              shell=True)

    return ()


def findNN(xy, point):
    """
    Find the index of the nearest neighbour of an array. 
    """
    mytree = spatial.cKDTree(xy)
    dist, indices = mytree.query(point)
    return indices

def sortPatch(patchPoints):
    """ 
    Sort the points on a patch by the nearest neighbour approach.
    """
    dummy = patchPoints
    for i in range(len(patchPoints)):
        if i==0:
            index = 0
            patchPoints[i, :] = dummy[index,:]
        else:
            findPoint = patchPoints[i-1]
            index = findNN(dummy, findPoint)
            patchPoints[i, :] = dummy[index,:]       
        # delete index from the dummy array to avoid points read twice.
        dummy = np.delete(dummy, index, axis=0)
    return patchPoints