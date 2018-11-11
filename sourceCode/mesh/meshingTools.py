import numpy as np

def ellipseGetX(a, b, theta):
    """
    This function can be used to find the x-point on an ellipse, given the angle theta, and the focal points a, b
    """
    x = a*b/np.sqrt(b*b + a*a*np.tan(theta)*np.tan(theta))
    return x

def ellipseGetY(a, b, x):
    """
    This function can be used to find the y-point on an ellipse, given the focal points a,b and the x-coordinate. 
    """
    y = b*np.sqrt(1- x*x/(a*a))
    return y
    
def getQuadPoints(a, b, angle, c, h):
    """
    This function can be used to create the coefficients for a parabolic curve from the wing to the outside of a parabola.
    enter: 
    a, b:   focal points
    angle:  topangle 
    c:      chord of the wing
    h:      width of the wing 
    """
    x1 = ellipseGetX(a, b, angle)   #point of the block
    y1 = ellipseGetY(a, b, x1)
    
    RHS = [[c/2.],[y1],[1.]]
    A = [[h*h/4., h/2., 1.],[x1*x1, x1, 1.],[h, 1., 0.]]
    coeffs = np.dot(np.linalg.inv(A), RHS) 
    return coeffs  
        
def rotCirc(circ, angle):
    """
    Function to rotate (circ??) by a angle. 
    """
    rot = np.array([[np.cos(angle), -np.sin(angle), 0],[np.sin(angle), np.cos(angle), 0],[0, 0, 1]]) 
    return np.dot(rot, circ.T)   

def writeVertices(f, coors):
    f.write("vertices\n(\n")
    for i in range(len(coors)):
        f.write("\t( " +str(coors[i,0]) + "  " + str(coors[i,1]) + "  " + str(coors[i,2]) + "  )\n")
    f.write(");\n")
    return 0

def writeCustomBlocks(f, coors, Ncoors):
    f.write("blocks\n(\n")
    
    blocks = np.empty((0,8), int)
    # inner circle
    niBlocks = 8
    elements = np.array([10, 10, 10])
    grading = np.array([1,1,1])
    pointsI = np.array([0, 8, 9, 1])
    pointIMax = np.array([8, 16, 16, 8])
    for i in range(niBlocks):
        points1 = pointsI+i
        bools = points1>(pointIMax-1)
        points1 = points1 - bools*niBlocks

        blockPoints = np.append(points1, points1+Ncoors)
        blocks = np.append(blocks, [blockPoints], axis=0)
        writeBlock(f, blockPoints, elements)

    f.write("\n")


    # outer circle
    noBlocks = 12
    elements = np.array([10, 10, 10])
    grading = np.array([1,1,1])
    pointsO = np.array([[10, 31, 16, 17],
                        [10, 17, 18, 11],
                        [11, 18, 19, 12],
                        [12, 19, 20, 21],
                        [12, 21, 22, 13],
                        [13, 22, 23, 14],
                        [14, 23, 24, 25],
                        [14, 25, 26, 15],
                        [15, 26, 27, 8],
                        [8, 27, 28, 29],
                        [8, 29, 30, 9],
                        [9, 30, 31, 10]]) 

    for i in range(len(pointsO)):
        points1 = pointsO[i,:]
        blockPoints = np.append(points1, points1+Ncoors)
        blocks = np.append(blocks, [blockPoints], axis=0)
        writeBlock(f, blockPoints, elements)
    
    f.write(");\n")
    return blocks


def writeBlock(f, points, elements, grading=np.array([1,1,1])):
    """
    Here you can write a block with the specified points, elements and an optional grading
    """
    f.write("\thex (   " )
    for point in points:
        f.write(str(int(point))+ "  ")
    f.write(" )\n\t\t( ")
    for element in elements:
        f.write(str(element)+ "  ")
    if len(grading)==3:
        f.write(" )\n\t\tsimpleGrading ( ")
        for grade in grading:
            f.write(str(grade) + "  ") 
        f.write(")\n")
    elif len(grading)==12:
        f.write(" )\n\t\tedgeGrading ( ")
        for grade in grading:
            f.write(str(grade) + "  ") 
        f.write(")\n")
    else:
        print("provide a valid grading criterion.")
        return 0
    return 0
        
def writeCustomEdges(f, coors, ellipseCoorsFile, Ncoors, span, widthMargin, arcCoors):
    f.write('#include "splineCoors.dat";\n')

    f.write("edges\n(\n")
    # =========================================================== #
    # First create the splineCoors
    print('running ellipseCoors.py. Check if the parameters are set correctly!!!')
    exec(open(ellipseCoorsFile).read())

    # polyLines part. 
    splineName = 'coor'
    splines  = [0, 1, 2]
    sides = ['symm', 'tip'] #, 'outer']
    sidesDict = {'symm':0, 'tip':span, 'outer':widthMargin}
    vsides = ['top', 'bottom']
    hsides = ['left', 'right']
    polyLines = np.array([
                        [10,  9],
                        [9,   8],
                        [1,   9],
                        [10, 11],
                        [11, 12],
                        [3,  11],
                        [14, 15],
                        [15,  8],
                        [7,  15],
                        [14, 13],
                        [13, 12],
                        [5,  13]])
    arcLines = np.array([
                    [0, 1],
                    [3, 4],
                    [4, 5],
                    [7, 0]])
    copyArcCoors = np.copy(arcCoors)
    for i in range(1,len(sides)):
        polyLines = np.append(polyLines, polyLines+Ncoors*i, axis=0)
        arcLines = np.append(arcLines, arcLines+Ncoors*i, axis=0)
        copyArcCoors[:,2]=sidesDict[sides[i]]
        arcCoors = np.append(arcCoors, copyArcCoors, axis=0)

    j=0
    for side in sides:                      # type of spline
        for hside in hsides:                # side z-directions
            for vside in vsides:            # left, right
                for spline in splines:      # top, bottom
                    name = splineName + str(spline) + side + hside + vside
                    f.write('\tpolyLine ' + str(polyLines[j,0]) + ' ' + str(polyLines[j,1]) + '  $'+name+'\n')
                    j+=1


    j=0
    for side in sides:
        for k in range(4):
            f.write('\tarc ' + str(arcLines[j,0]) + ' ' + str(arcLines[j,1]) + ' ( ' + str(arcCoors[j,0]) + ' ' + str(arcCoors[j,1]) + ' ' + str(arcCoors[j,2]) +' )\n')
            j+=1

    f.write(");\n")
    return 0

def writeBoundary(f, coors):
    f.write("boundary\n(\n")
    
    f.write(");\n")
    return 0

def writeMergePatchPars(f):
    f.write("mergePatchPairs\n(\n")
    f.write(");\n")
    return 0



    # Steps:
#1. Write the vertices
#2. Write the grading
#3. write the blocks
#4. include the splineCoors.dat
#5. write the edges
#6. write the boundary
#7. end with mergePatchPairs.