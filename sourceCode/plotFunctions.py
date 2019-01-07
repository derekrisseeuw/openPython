import matplotlib.pyplot as plt
#from matplotlib import rcParams
import matplotlib
import numpy as np
from PyFOAM_custom.PyFOAM_custom import getRANSVectorBoundary, sortPatch
import matplotlib.path as mpltPath
from postProcessing import getPeriod
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from scipy.interpolate import interp1d


def latexify(fig_width=None, fig_height=None, columns=2, type='line',
             width_multiplier=1, height_multiplier=1):
    # Reference Latexify from:
    # https://nipunbatra.github.io/blog/2014/latexify.html
    # Modified by Javier Fatou Gomez.
             
    """
    Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    type : countour of line, optional
    width_multiplier : set the right width
    height_multiplier : to diverged from golden ratio   
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates
    # # /transactions_art_guide.pdf
    page_width = 6.22
    assert(columns in [1,2])

    if fig_width is None:
        if columns==2:
            if type=='line':
                fig_width = page_width*1.0/2.*width_multiplier
            elif type=='contour':
                fig_width = page_width*1.08/2.*width_multiplier        
        elif columns==1:
            if type=='line':
                fig_width = page_width*0.7*width_multiplier
            elif type=='contour':
                fig_width = page_width*0.9*width_multiplier
        else:
            fig_width = page_width # width in inches

    if fig_height is None:
        golden_mean = (np.sqrt(5)-1.0)/2.0    # Aesthetic ratio
        if type=='line':
            fig_height = fig_width*1.2*golden_mean*height_multiplier # height in inches
        if type=='contour':
            fig_height = fig_width*height_multiplier # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              'text.latex.preamble': [r'\usepackage{gensymb, amsmath, siunitx}'],
              'axes.labelsize': 10,
              'axes.titlesize': 10,
              'font.size': 10,
              'legend.fontsize': 10,
              'xtick.labelsize': 9,
              'ytick.labelsize': 9,
              'xtick.major.size' : 4,
              'xtick.minor.size' : 2,
              'ytick.major.size' : 3,
              'ytick.minor.size' : 1.5,
              'xtick.major.width' : 0.5,
              'xtick.minor.width' : 0.5,
              'ytick.major.width' : 0.5,
              'ytick.minor.width' : 0.5,
              'xtick.direction': 'in',
              'ytick.direction': 'in',
              'text.usetex': True,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif',
              'lines.linewidth': 0.5,
              'grid.linewidth': 0.5,
              'grid.linestyle': 'None', #'dotted',
              'figure.autolayout': True,         # added to allways show the axis
    }

    matplotlib.rcParams.update(params)
    
    if type=='line':
        params_add = {
            'xtick.major.top' : True,
              'xtick.major.bottom' : True,
              'ytick.major.left' : True,
              'ytick.major.right' : True,
              'xtick.minor.top' : True,
              'xtick.minor.bottom' : True,
              'ytick.minor.left' : True,
              'ytick.minor.right' : True,
              'axes.spines.top': False,
              'axes.spines.right': False,
              'axes.spines.left': True,
              'axes.spines.bottom': True,
              'axes.grid': True,
        }
        matplotlib.rcParams.update(params_add)
        
    elif type=='contour':
        params_add = {
            'xtick.major.top' : False,
              'xtick.major.bottom' : True,
              'ytick.major.left' : True,
              'ytick.major.right' : False,
              'xtick.minor.top' : False,
              'xtick.minor.bottom' : False,
              'ytick.minor.left' : False,
              'ytick.minor.right' : False,
              'lines.linewidth': 0.,
              'axes.spines.bottom': True,
              'axes.spines.top': False,
              'axes.spines.left': True,
              'axes.spines.right': False,
              
              'axes.xmargin': 0.1,
              'axes.ymargin': 0.01,
        }
        matplotlib.rcParams.update(params_add)

    return ()

def linePlot(x, y, title=None, xlabel=None, ylabel=None, columns=2, 
             dashed=False, plotType='plot', axisStyle='sci', mark=None, height_multiplier=1.):
    #plt.close('all')
#    from functions import latexify
    latexify(columns=columns, type='line', width_multiplier=1.03, height_multiplier=height_multiplier)
    
    if plotType=='plot':
        if dashed==True:
            figName = plt.plot(x, y, '--')
        else:
            figName = plt.plot(x, y)
        plt.ticklabel_format(style=axisStyle, axis='both', scilimits=(0,1))
    elif plotType=='semilogx':
        if dashed==True:
            figName = plt.semilogx(x, y, '--')
        else:
            figName = plt.semilogx(x, y)
    elif plotType=='semilogy':
        if dashed==True:
            figName = plt.semilogy(x, y, '--')
        else:
            figName = plt.semilogy(x, y)
    elif plotType=='loglog':
        if dashed==True:
            figName = plt.loglog(x, y, '--')
        else:
            figName = plt.loglog(x, y)      
    plt.setp(figName[0],  
             marker=mark,
             markersize=4.,
             fillstyle='none')
    
    
    if title is not None:
        plt.title(title)        
    if xlabel is not None:
        plt.xlabel(xlabel)    
    if ylabel is not None:
        plt.ylabel(ylabel)
    return(figName)

def pointPlot(x, y, mark='p', title=None, xlabel=None, ylabel=None, columns=2, 
            plotType='plot', axisStyle='sci'):
    #plt.close('all')
#    from functions import latexify
    latexify(columns=columns, type='line', width_multiplier=1.03, height_multiplier=1)

    if plotType=='plot':
        figName, = plt.plot(x, y, mark, linestyle='None')
        plt.ticklabel_format(style=axisStyle, axis='x') #,  scilimits=(0,0))
        plt.ticklabel_format(style=axisStyle, axis='y') #, scilimits=(0,0))
    elif plotType=='semilogx':
        figName, = plt.semilogx(x, y, mark, linestyle='None')
    elif plotType=='semilogy':
        figName, = plt.semilogy(x, y, mark, linestyle='None')
    elif plotType=='loglog':
        figName, = plt.loglog(x, y, mark, linestyle='None') 
    
    plt.setp(figName[0],  
         markersize=4.,
         fillstyle='none')

    if title is not None:
        plt.title(title)
        
    if xlabel is not None:
        plt.xlabel(xlabel)
    
    if ylabel is not None:
        plt.ylabel(ylabel)
#    plt.tight_layout(w_pad=0.5, h_pad=-1.0)
    return(figName)

def contourPlot(x, y, z, title=None, xlabel=None, ylabel=None, columns=2, levels=None, height_multiplier=1):
    #plt.close('all')
#    from functions import latexify
    latexify(columns=columns, type='contour', width_multiplier=1.00, height_multiplier=height_multiplier)
    
    plt.axis('equal')
    
    figName = plt.contourf(x, y, z, extend='both')
    if title is not None:
        plt.title(title)       
    if xlabel is not None:
        plt.xlabel(xlabel)   
    if ylabel is not None:
        plt.ylabel(ylabel)
    if levels is not None:
        figName = plt.contour(figName, levels=levels)
    
    return(figName)

def addOpacity(cmap, opacityArray, plotLevels):
    """ 
    This function adds opacity to a colorbar
    Arguments: cmap
    opacity numpy array with x-range and opacity function
    """
    newCmap = cmap(np.arange(cmap.N))  # cmap.N
    x = opacityArray[0]
    y = opacityArray[1]
    xmap = np.linspace(np.min(x), np.max(x), cmap.N)
    ymap = np.interp(xmap, x, y)
    newCmap[:,-1] = ymap  
    return ListedColormap(newCmap)

def cont_cool(meshx, meshy, var, cbar_label, plot_levels, plot_limits=None,
              cmap_name=None, filename="contourPlot", columns=2,
              contours_folder="figures", opacity=None):
    """
    Plot filled contours of a variable in RANS mesh.
    Parameters
    ----------
    meshx, meshy : ndarray
        x, y coordinates of mesh in read_RANS_mesh format.
    var : ndarray
        Variable to plot.
    plot_limits : list
        Maximum and minimum values of the contour plot.
    plot_levels : integer
        Number of levels for the contours.
    cmap_name : string
        Name of the colormap. 
    cbar_label : string
        Label for the colorbar. If none, no colorbar is plotted. 
    filename : string
        Name of the file containing the contour plot.
    contours_folder : string
        Directory where the plot will be saved.

    Returns
    -------

    """
    plt.close('all')
    
    latexify(columns=columns, type='contour')
    
    if plot_limits is None:
        plot_limits=[np.min(var[~np.isnan(var)]), np.max(var[~np.isnan(var)])]
    plotRange = plot_limits[1]  - plot_limits[0] 
    if cmap_name is None:
        cmap_name = "jet"
        
    if opacity is not None:
        cmap = mpl.cm.get_cmap(cmap_name)
        cmap = addOpacity(cmap, opacity, plot_levels)
    else:
        cmap = cmap_name
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    plot_levels_array = np.linspace(plot_limits[0], plot_limits[1],
                                    plot_levels)
    plot_fig = ax.contourf(meshx, meshy, var, plot_levels_array,
                           extend="both", cmap=cmap)
#    ax.axis((np.min(meshx), np.max(meshx),
#             0, np.max(meshy)))

#    ax.set_aspect('auto', adjustable=None)
    # Remove ticks but keep labels.
    ax.tick_params(top=False, bottom=False, left=False, right=False,
                   labelleft=True, labelbottom=True)
#    ax.set_xlabel(r'$x/c [-]$')
#    ax.set_ylabel(r'$y/c [-]$')
    
    ax.set_xlabel(r'r/R [-]')
    ax.set_ylabel(r'$t^*$ [-]')
    ax.xaxis.labelpad -= 4
#    print("plotLimits are: " + str(plot_limits))
    # Move the label of x axis a bit up.

    # Colorbar parameters.
    m0=plot_limits[0]            # colorbar min value
    m4=plot_limits[-1]             # colorbar max value
    if columns==1:
        num_ticks = 5
    else:
        num_ticks = 4
    # to get ticks
    # we need a small offset from the maximum value...
    ticks = np.round(np.linspace(m0, m4-0.001*plotRange, num_ticks), 4)  
    
    # get labels.
    if plotRange >= 500.:
        numLabels = np.round(np.linspace(m0, m4, num_ticks), 3)
        labels = ["a"]*num_ticks
        pow = int(("%e" % max(abs(numLabels))).split("+")[-1])
        for i in range(len(labels)):
            labels[i] = ("%.1f" % (numLabels[i]/float(10**pow)) + r"$\cdot 10^{%i}$" % pow)
    else:            
        labels = np.round(np.linspace(m0, m4, num_ticks), 3) 
    
    if cbar_label is not None:
        cbar = fig.colorbar(plot_fig,
                            orientation='horizontal', shrink=0.6)
    
        cbar.set_label(cbar_label)
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(labels)
    
        # Control the lines inside the colorbar.
        if columns==1:
            tickSize = 9.2
        else:
            tickSize = 5    
        cbar.ax.tick_params(colors='k', size=tickSize, direction='in',
                            zorder=10, width=0.3)
        # Move the colorbar slightly up.
        l, b, w, h = plt.gca().get_position().bounds
        ll, bb, ww, hh = cbar.ax.get_position().bounds
        if columns==1:
            cbar.ax.set_position([ll, b-.55, ww, h*0.01])
        else:
            cbar.ax.set_position([ll, b-.35, ww, h*0.01])
            
        # Set linewidths for colorbar and axes box.
        cbar.outline.set_linewidth(0.5)
#    [i.set_linewidth(0.15) for i in ax.spines.itervalues()]
    return fig
#    fig.savefig(contours_folder + '/' + filename + '.pdf',
#                bbox_inches='tight')
#    plt.close('all')


def circleInternalPoints(mesh, point, radius):
    return np.sqrt(((mesh[0]-point[0])**2) + ((mesh[1]-point[1])**2)) < radius

def patchInternalPoints(mesh, patch, case_dir, time):
    var = "C"
    selected_wall=patch
    boundaryData = getRANSVectorBoundary(case_dir, time, var, selected_wall)
    
    #plt.scatter(v[0,:], v[1,:])
    patchPoints = np.vstack((boundaryData[0,:], boundaryData[1,:])).T
    if patch == 'flap':
        patchPoints = np.insert(patchPoints, 0, [0.2, 0.19], axis=0)
        patchPoints = np.insert(patchPoints, len(patchPoints), [0.2, 0.21], axis=0)
    
    flapPath = mpltPath.Path(patchPoints)
    # sort the points according to NN. 
    patchPoints = sortPatch(patchPoints)
    
    plotPoints = np.hstack((np.expand_dims(np.concatenate(mesh[0]), axis=0).T, 
                       np.expand_dims(np.concatenate(mesh[1]), axis=0).T))
    
    interiorFlap = flapPath.contains_points(plotPoints).reshape((len(mesh[0,:]), len(mesh[0,0])))
    return interiorFlap

def maskFlap(mesh, Z, case_dir, time):
    """
    Mask a patch
    ---
    parameters:
        mesh
        Z
        patch
        case_dir
        time
    """
    interiorCircle = circleInternalPoints(mesh, point=np.array([0.2, 0.2]), radius = 0.05)
    interiorPatch = patchInternalPoints(mesh, "flap", case_dir, time)
    Z[interiorCircle] = np.nan #np.ma.masked
    Z[interiorPatch] = np.nan #np.ma.masked
    return Z


def maskPatch(mesh, Z, patch, case_dir, time):
    """
    Mask a patch
    ---
    parameters:
        mesh
        Z
        patch
        case_dir
        time
    """
    interiorPatch = patchInternalPoints(mesh, patch, case_dir, time)
    Z[interiorPatch] = np.nan #np.ma.masked
    return Z

def getCustomCmap(x, r, g, b, N = 256):
    customCmap =  np.ones((N, 4))
    xmap = np.linspace(np.min(x), np.max(x), N)
    interp ='linear'
    fr, fg, fb = interp1d(x, r, interp), interp1d(x, g, interp), interp1d(x, b, interp)
    customCmap[ :,0] = fr(xmap)
    customCmap[ :,1] = fg(xmap)
    customCmap[ :,2] = fb(xmap)
    return customCmap

def paraviewJet(N = 256):
    x = np.array([-1, -0.777778, -0.269841, -0.015873,0.238095, 0.746032, 1])
    r = np.array([0, 0, 0, 0.5, 1, 1, 0.5])
    g = np.array([0, 0, 1, 1, 1, 0, 0])
    b = np.array([0.5625,  1, 1, 0.5, 0, 0, 0 ])
    return getCustomCmap(x, r, g, b, N)

def paraviewRainbow(N = 256):
    x = np.array([ -1.,-0.5, 0., 0.5, 1.])
    r = np.array([0,0,0,1,1])
    g = np.array([0,1,1,1,0])
    b = np.array([1.,1,0,0, 0])
    return getCustomCmap(x, r, g, b, N)

def paraviewCoolwarm(N = 256):
    x = np.array([0, 1])
    r = np.array([0,1])
    g = np.array([0.,0])
    b = np.array([1., 0])
    return getCustomCmap(x, r, g, b, N) 




    
if __name__ == "__main__":
#    from functions import linePlot
    x = np.linspace(0, 10, 100)
    y = np.cos(x)*1.1
    
    figureA, ax = plt.figure(1)
    linePlot(x, y, xlabel='asdfasdf', ylabel=r'Some with $a_{\beta}$', columns=1)
    print(figureA[0])
    figAName = '/home/derek/Dropbox/thesis/figures/tryFig2.pdf'
    plt.savefig(figAName, format='pdf')
    plt.close(figureA)
    plt.show()
    
    

