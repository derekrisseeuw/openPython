import matplotlib.pyplot as plt
#from matplotlib import rcParams
import matplotlib
import numpy as np
from PyFOAM_custom.PyFOAM_custom import getRANSVectorBoundary, sortPatch
import matplotlib.path as mpltPath
from postProcessing import getPeriod

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
              'text.latex.preamble': [r'\usepackage{gensymb}'],
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
              'xtick.major.bottom' : False,
              'ytick.major.left' : False,
              'ytick.major.right' : False,
              'xtick.minor.top' : False,
              'xtick.minor.bottom' : False,
              'ytick.minor.left' : False,
              'ytick.minor.right' : False,
              'lines.linewidth': 0.,
              'axes.spines.bottom': False,
              'axes.spines.top': False,
              'axes.spines.left': False,
              'axes.spines.right': False,
              
              'axes.xmargin': 0.1,
              'axes.ymargin': 0.01,
        }
        matplotlib.rcParams.update(params_add)

    return ()
    

def my_formatter_fun(x, p):
    scale_pow=2
    return "%.2f" % (x * (10 ** scale_pow))

def linePlot(x, y, title=None, xlabel=None, ylabel=None, columns=2, 
             dashed=False, plotType='plot', axisStyle='sci'):
    #plt.close('all')
#    from functions import latexify
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
    
    
    plt.ticklabel_format(style=axisStyle, axis='x', scilimits=(0,0))
    plt.ticklabel_format(style=axisStyle, axis='y', scilimits=(0,0))
    
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
        figName, = plt.plot(x, y, mark, markersize=.2, linestyle='None')
    elif plotType=='semilogx':
        figName, = plt.semilogx(x, y, 'p')    
    elif plotType=='semilogy':
        figName, = plt.semilogy(x, y, 'p') 
    elif plotType=='loglog':
        figName, = plt.loglog(x, y, 'p') 
        
    plt.ticklabel_format(style=axisStyle, axis='x', scilimits=(0,0))
    plt.ticklabel_format(style=axisStyle, axis='y', scilimits=(0,0))

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


def cont_cool(meshx, meshy, var, cbar_label, plot_levels, plot_limits=None,
              cmap_name=None, filename="contourPlot", columns=2,
              contours_folder="figures"):
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
        Label for the colorbar.
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
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    plot_levels_array = np.linspace(plot_limits[0], plot_limits[1],
                                    plot_levels)
    plot_fig = ax.contourf(meshx, meshy, var, plot_levels_array,
                           extend="both", cmap=cmap_name)
#    ax.axis((np.min(meshx), np.max(meshx),
#             0, np.max(meshy)))

#    ax.set_aspect('auto', adjustable=None)
    # Remove ticks but keep labels.
    ax.tick_params(top=False, bottom=False, left=False, right=False,
                   labelleft=True, labelbottom=True)
    ax.set_xlabel(r'$x [m]$')
    ax.set_ylabel(r'$y [m]$')
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
    ll, bb, ww, hh =cbar.ax.get_position().bounds
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
    
    
    
'''
RcParams({'_internal.classic_mode': False,
          'agg.path.chunksize': 0,
          'animation.avconv_args': [],
          'animation.avconv_path': 'avconv',
          'animation.bitrate': -1,
          'animation.codec': 'h264',
          'animation.convert_args': [],
          'animation.convert_path': 'convert',
          'animation.embed_limit': 20.0,
          'animation.ffmpeg_args': [],
          'animation.ffmpeg_path': 'ffmpeg',
          'animation.frame_format': 'png',
          'animation.html': 'none',
          'animation.html_args': [],
          'animation.writer': 'ffmpeg',
          'axes.autolimit_mode': 'data',
          'axes.axisbelow': 'line',
          'axes.edgecolor': 'k',
          'axes.facecolor': 'w',
          'axes.formatter.limits': [-7, 7],
          'axes.formatter.min_exponent': 0,
          'axes.formatter.offset_threshold': 4,
          'axes.formatter.use_locale': False,
          'axes.formatter.use_mathtext': False,
          'axes.formatter.useoffset': True,
          'axes.grid': False,
          'axes.grid.axis': 'both',
          'axes.grid.which': 'major',
          'axes.hold': None,
          'axes.labelcolor': 'k',
          'axes.labelpad': 4.0,
          'axes.labelsize': 10.0,
          'axes.labelweight': 'normal',
          'axes.linewidth': 0.8,
          'axes.prop_cycle': cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']),
          'axes.spines.bottom': False,
          'axes.spines.left': False,
          'axes.spines.right': False,
          'axes.spines.top': True,
          'axes.titlepad': 6.0,
          'axes.titlesize': 10.0,
          'axes.titleweight': 'normal',
          'axes.unicode_minus': True,
          'axes.xmargin': 0.05,
          'axes.ymargin': 0.05,
          'axes3d.grid': True,
          'backend': 'ps',
          'backend.qt4': None,
          'backend.qt5': None,
          'backend_fallback': True,
          'boxplot.bootstrap': None,
          'boxplot.boxprops.color': 'k',
          'boxplot.boxprops.linestyle': '-',
          'boxplot.boxprops.linewidth': 1.0,
          'boxplot.capprops.color': 'k',
          'boxplot.capprops.linestyle': '-',
          'boxplot.capprops.linewidth': 1.0,
          'boxplot.flierprops.color': 'k',
          'boxplot.flierprops.linestyle': 'none',
          'boxplot.flierprops.linewidth': 1.0,
          'boxplot.flierprops.marker': 'o',
          'boxplot.flierprops.markeredgecolor': 'k',
          'boxplot.flierprops.markerfacecolor': 'none',
          'boxplot.flierprops.markersize': 6.0,
          'boxplot.meanline': False,
          'boxplot.meanprops.color': 'C2',
          'boxplot.meanprops.linestyle': '--',
          'boxplot.meanprops.linewidth': 1.0,
          'boxplot.meanprops.marker': '^',
          'boxplot.meanprops.markeredgecolor': 'C2',
          'boxplot.meanprops.markerfacecolor': 'C2',
          'boxplot.meanprops.markersize': 6.0,
          'boxplot.medianprops.color': 'C1',
          'boxplot.medianprops.linestyle': '-',
          'boxplot.medianprops.linewidth': 1.0,
          'boxplot.notch': False,
          'boxplot.patchartist': False,
          'boxplot.showbox': True,
          'boxplot.showcaps': True,
          'boxplot.showfliers': True,
          'boxplot.showmeans': False,
          'boxplot.vertical': True,
          'boxplot.whiskerprops.color': 'k',
          'boxplot.whiskerprops.linestyle': '-',
          'boxplot.whiskerprops.linewidth': 1.0,
          'boxplot.whiskers': 1.5,
          'contour.corner_mask': True,
          'contour.negative_linestyle': 'dashed',
          'datapath': '/home/derek/anaconda3/lib/python3.6/site-packages/matplotlib/mpl-data',
          'date.autoformatter.day': '%Y-%m-%d',
          'date.autoformatter.hour': '%m-%d %H',
          'date.autoformatter.microsecond': '%M:%S.%f',
          'date.autoformatter.minute': '%d %H:%M',
          'date.autoformatter.month': '%Y-%m',
          'date.autoformatter.second': '%H:%M:%S',
          'date.autoformatter.year': '%Y',
          'docstring.hardcopy': False,
          'errorbar.capsize': 0.0,
          'examples.directory': '',
          'figure.autolayout': True,
          'figure.constrained_layout.h_pad': 0.04167,
          'figure.constrained_layout.hspace': 0.02,
          'figure.constrained_layout.use': False,
          'figure.constrained_layout.w_pad': 0.04167,
          'figure.constrained_layout.wspace': 0.02,
          'figure.dpi': 72.0,
          'figure.edgecolor': 'white',
          'figure.facecolor': 'white',
          'figure.figsize': [5.598, 0.9180719999999999],
          'figure.frameon': True,
          'figure.max_open_warning': 20,
          'figure.subplot.bottom': 0.125,
          'figure.subplot.hspace': 0.2,
          'figure.subplot.left': 0.125,
          'figure.subplot.right': 0.9,
          'figure.subplot.top': 0.88,
          'figure.subplot.wspace': 0.2,
          'figure.titlesize': 'large',
          'figure.titleweight': 'normal',
          'font.cursive': ['Apple Chancery',
                           'Textile',
                           'Zapf Chancery',
                           'Sand',
                           'Script MT',
                           'Felipa',
                           'cursive'],
          'font.family': ['serif'],
          'font.fantasy': ['Comic Sans MS',
                           'Chicago',
                           'Charcoal',
                           'ImpactWestern',
                           'Humor Sans',
                           'xkcd',
                           'fantasy'],
          'font.monospace': ['DejaVu Sans Mono',
                             'Bitstream Vera Sans Mono',
                             'Computer Modern Typewriter',
                             'Andale Mono',
                             'Nimbus Mono L',
                             'Courier New',
                             'Courier',
                             'Fixed',
                             'Terminal',
                             'monospace'],
          'font.sans-serif': ['DejaVu Sans',
                              'Bitstream Vera Sans',
                              'Computer Modern Sans Serif',
                              'Lucida Grande',
                              'Verdana',
                              'Geneva',
                              'Lucid',
                              'Arial',
                              'Helvetica',
                              'Avant Garde',
                              'sans-serif'],
          'font.serif': ['DejaVu Serif',
                         'Bitstream Vera Serif',
                         'Computer Modern Roman',
                         'New Century Schoolbook',
                         'Century Schoolbook L',
                         'Utopia',
                         'ITC Bookman',
                         'Bookman',
                         'Nimbus Roman No9 L',
                         'Times New Roman',
                         'Times',
                         'Palatino',
                         'Charter',
                         'serif'],
          'font.size': 10.0,
          'font.stretch': 'normal',
          'font.style': 'normal',
          'font.variant': 'normal',
          'font.weight': 'normal',
          'grid.alpha': 1.0,
          'grid.color': '#b0b0b0',
          'grid.linestyle': 'dotted',
          'grid.linewidth': 0.5,
          'hatch.color': 'k',
          'hatch.linewidth': 1.0,
          'hist.bins': 10,
          'image.aspect': 'equal',
          'image.cmap': 'viridis',
          'image.composite_image': True,
          'image.interpolation': 'nearest',
          'image.lut': 256,
          'image.origin': 'upper',
          'image.resample': True,
          'interactive': True,
          'keymap.all_axes': ['a'],
          'keymap.back': ['left', 'c', 'backspace'],
          'keymap.forward': ['right', 'v'],
          'keymap.fullscreen': ['f', 'ctrl+f'],
          'keymap.grid': ['g'],
          'keymap.grid_minor': ['G'],
          'keymap.home': ['h', 'r', 'home'],
          'keymap.pan': ['p'],
          'keymap.quit': ['ctrl+w', 'cmd+w', 'q'],
          'keymap.quit_all': ['W', 'cmd+W', 'Q'],
          'keymap.save': ['s', 'ctrl+s'],
          'keymap.xscale': ['k', 'L'],
          'keymap.yscale': ['l'],
          'keymap.zoom': ['o'],
          'legend.borderaxespad': 0.5,
          'legend.borderpad': 0.4,
          'legend.columnspacing': 2.0,
          'legend.edgecolor': '0.8',
          'legend.facecolor': 'inherit',
          'legend.fancybox': True,
          'legend.fontsize': 10.0,
          'legend.framealpha': 0.8,
          'legend.frameon': True,
          'legend.handleheight': 0.7,
          'legend.handlelength': 2.0,
          'legend.handletextpad': 0.8,
          'legend.labelspacing': 0.5,
          'legend.loc': 'best',
          'legend.markerscale': 1.0,
          'legend.numpoints': 1,
          'legend.scatterpoints': 1,
          'legend.shadow': False,
          'lines.antialiased': True,
          'lines.color': 'C0',
          'lines.dash_capstyle': 'butt',
          'lines.dash_joinstyle': 'round',
          'lines.dashdot_pattern': [6.4, 1.6, 1.0, 1.6],
          'lines.dashed_pattern': [3.7, 1.6],
          'lines.dotted_pattern': [1.0, 1.65],
          'lines.linestyle': '-',
          'lines.linewidth': 0.0,
          'lines.marker': 'None',
          'lines.markeredgewidth': 1.0,
          'lines.markersize': 6.0,
          'lines.scale_dashes': True,
          'lines.solid_capstyle': 'projecting',
          'lines.solid_joinstyle': 'round',
          'markers.fillstyle': 'full',
          'mathtext.bf': 'sans:bold',
          'mathtext.cal': 'cursive',
          'mathtext.default': 'it',
          'mathtext.fallback_to_cm': True,
          'mathtext.fontset': 'dejavusans',
          'mathtext.it': 'sans:italic',
          'mathtext.rm': 'sans',
          'mathtext.sf': 'sans',
          'mathtext.tt': 'monospace',
          'patch.antialiased': True,
          'patch.edgecolor': 'k',
          'patch.facecolor': 'C0',
          'patch.force_edgecolor': False,
          'patch.linewidth': 1.0,
          'path.effects': [],
          'path.simplify': True,
          'path.simplify_threshold': 0.1111111111111111,
          'path.sketch': None,
          'path.snap': True,
          'pdf.compression': 6,
          'pdf.fonttype': 3,
          'pdf.inheritcolor': False,
          'pdf.use14corefonts': False,
          'pgf.debug': False,
          'pgf.preamble': [],
          'pgf.rcfonts': True,
          'pgf.texsystem': 'xelatex',
          'polaraxes.grid': True,
          'ps.distiller.res': 6000,
          'ps.fonttype': 3,
          'ps.papersize': 'letter',
          'ps.useafm': False,
          'ps.usedistiller': False,
          'savefig.bbox': None,
          'savefig.directory': '~',
          'savefig.dpi': 'figure',
          'savefig.edgecolor': 'w',
          'savefig.facecolor': 'w',
          'savefig.format': 'png',
          'savefig.frameon': True,
          'savefig.jpeg_quality': 95,
          'savefig.orientation': 'portrait',
          'savefig.pad_inches': 0.1,
          'savefig.transparent': False,
          'scatter.marker': 'o',
          'svg.fonttype': 'path',
          'svg.hashsalt': None,
          'svg.image_inline': True,
          'text.antialiased': True,
          'text.color': 'k',
          'text.hinting': 'auto',
          'text.hinting_factor': 8,
          'text.latex.preamble': ['\\usepackage{gensymb}'],
          'text.latex.preview': False,
          'text.latex.unicode': False,
          'text.usetex': True,
          'timezone': 'UTC',
          'tk.window_focus': False,
          'toolbar': 'toolbar2',
          'verbose.fileo': 'sys.stdout',
          'verbose.level': 'silent',
          'webagg.address': '127.0.0.1',
          'webagg.open_in_browser': True,
          'webagg.port': 8988,
          'webagg.port_retries': 50,
          'xtick.alignment': 'center',
          'xtick.bottom': True,
          'xtick.color': 'k',
          'xtick.direction': 'in',
          'xtick.labelbottom': True,
          'xtick.labelsize': 9.0,
          'xtick.labeltop': False,
          'xtick.major.bottom': False,
          'xtick.major.pad': 3.5,
          'xtick.major.size': 4.0,
          'xtick.major.top': False,
          'xtick.major.width': 0.5,
          'xtick.minor.bottom': False,
          'xtick.minor.pad': 3.4,
          'xtick.minor.size': 2.0,
          'xtick.minor.top': False,
          'xtick.minor.visible': False,
          'xtick.minor.width': 0.5,
          'xtick.top': False,
          'ytick.alignment': 'center_baseline',
          'ytick.color': 'k',
          'ytick.direction': 'in',
          'ytick.labelleft': True,
          'ytick.labelright': False,
          'ytick.labelsize': 9.0,
          'ytick.left': True,
          'ytick.major.left': False,
          'ytick.major.pad': 3.5,
          'ytick.major.right': False,
          'ytick.major.size': 3.0,
          'ytick.major.width': 0.5,
          'ytick.minor.left': False,
          'ytick.minor.pad': 3.4,
          'ytick.minor.right': False,
          'ytick.minor.size': 1.5,
          'ytick.minor.visible': False,
          'ytick.minor.width': 0.5,
          'ytick.right': False})
'''
