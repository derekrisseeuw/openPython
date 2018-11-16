import matplotlib.pyplot as plt
#from matplotlib import rcParams
import matplotlib
import numpy as np

def latexify(fig_width=None, fig_height=None, columns=2, type='line',
             width_multiplier=1, height_multiplier=1):
    # Reference Latexify from:
    # https://nipunbatra.github.io/blog/2014/latexify.html
    # Modified by Javier Fatou Gomez.
             
    """Set up matplotlib's RC params for LaTeX plotting.
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
                fig_width = page_width*0.74*width_multiplier
        else:
            fig_width = page_width # width in inches

    if fig_height is None:
        golden_mean = (np.sqrt(5)-1.0)/2.0    # Aesthetic ratio
        if type=='line':
            fig_height = fig_width*1.2*golden_mean*height_multiplier # height in inches
        if type=='contour':
            fig_height = fig_width*1.6*golden_mean*height_multiplier # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              'text.latex.preamble': ['\usepackage{gensymb}'],
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
              'grid.linestyle': 'dotted',
              'figure.autolayout': True         # added to allways show the axis
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
        }
        matplotlib.rcParams.update(params_add)
        
    elif type=='contour':
        params_add = {
            'xtick.major.top' : False,
              'xtick.major.bottom' : False,
              'ytick.major.left' : False,
              'ytick.major.right' : False,
              'xtick.minor.top' : False,
              'xtick.minor.bottom' : False,
              'ytick.minor.left' : False,
              'ytick.minor.right' : False,
        }
        matplotlib.rcParams.update(params_add)

    return ()
    
    
def linePlot(x, y, title=None, xlabel=None, ylabel=None, columns=2, dashed=False, plotType='plot'):
    #plt.close('all')
    from functions import latexify
    latexify(columns=columns, type='line', width_multiplier=1.03, height_multiplier=1)

    if plotType=='plot':
        if dashed==True:
            figName = plt.plot(x, y, '--')
        else:
            figName = plt.plot(x, y)
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

    if title is not None:
        plt.title(title)        
    if xlabel is not None:
        plt.xlabel(xlabel)    
    if ylabel is not None:
        plt.ylabel(ylabel)
    return(figName)

def pointPlot(x, y, title=None, xlabel=None, ylabel=None, columns=2, plotType='plot'):
    #plt.close('all')
    from functions import latexify
    latexify(columns=columns, type='line', width_multiplier=1.03, height_multiplier=1)
    
    if plotType=='plot':
        figName, = plt.plot(x, y, 'p')
    elif plotType=='semilogx':
        figName, = plt.semilogx(x, y, 'p')    
    elif plotType=='semilogy':
        figName, = plt.semilogy(x, y, 'p') 
    elif plotType=='loglog':
        figName, = plt.loglog(x, y, 'p') 
        
    if title is not None:
        plt.title(title)
        
    if xlabel is not None:
        plt.xlabel(xlabel)
    
    if ylabel is not None:
        plt.ylabel(ylabel)
#    plt.tight_layout(w_pad=0.5, h_pad=-1.0)
    return(figName)

def contourPlot(x, y, title=None, xlabel=None, ylabel=None, columns=2):
    #plt.close('all')
    from functions import latexify
    latexify(columns=columns, type='contour', width_multiplier=1.03, height_multiplier=1)
    
    figName, = plt.plot(x, y)
    if title is not None:
        plt.title(title)       
    if xlabel is not None:
        plt.xlabel(xlabel)   
    if ylabel is not None:
        plt.ylabel(ylabel)
    
    return(figName)

    
if __name__ == "__main__":
    from functions import linePlot
    x = np.linspace(0, 10, 100)
    y = np.cos(x)*1.1
    
    figureA, = plt.figure(1)
    linePlot(x, y, xlabel='asdfasdf', ylabel=r'Some with $a_{\beta}$', columns=1)
    figAName = '/home/derek/Dropbox/thesis/figures/tryFig2.pdf'
    plt.savefig(figAName, format='pdf')
    plt.close(figureA)
    plt.show()
