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
    