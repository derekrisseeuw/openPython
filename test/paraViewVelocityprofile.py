#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
comFlow5FineOpenFOAM = GetActiveSource()

# Properties modified on comFlow5FineOpenFOAM
comFlow5FineOpenFOAM.Skip0time = 0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [990, 860]

# show data in view
comFlow5FineOpenFOAMDisplay = Show(comFlow5FineOpenFOAM, renderView1)
# trace defaults for the display properties.
comFlow5FineOpenFOAMDisplay.Representation = 'Surface'
comFlow5FineOpenFOAMDisplay.ColorArrayName = [None, '']
comFlow5FineOpenFOAMDisplay.OSPRayScaleArray = 'U'
comFlow5FineOpenFOAMDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
comFlow5FineOpenFOAMDisplay.SelectOrientationVectors = 'None'
comFlow5FineOpenFOAMDisplay.ScaleFactor = 0.040002635121345526
comFlow5FineOpenFOAMDisplay.SelectScaleArray = 'None'
comFlow5FineOpenFOAMDisplay.GlyphType = 'Arrow'
comFlow5FineOpenFOAMDisplay.GlyphTableIndexArray = 'None'
comFlow5FineOpenFOAMDisplay.DataAxesGrid = 'GridAxesRepresentation'
comFlow5FineOpenFOAMDisplay.PolarAxes = 'PolarAxesRepresentation'
comFlow5FineOpenFOAMDisplay.ScalarOpacityUnitDistance = 0.007633165601343383
comFlow5FineOpenFOAMDisplay.GaussianRadius = 0.020001317560672763
comFlow5FineOpenFOAMDisplay.SetScaleArray = ['POINTS', 'p']
comFlow5FineOpenFOAMDisplay.ScaleTransferFunction = 'PiecewiseFunction'
comFlow5FineOpenFOAMDisplay.OpacityArray = ['POINTS', 'p']
comFlow5FineOpenFOAMDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(comFlow5FineOpenFOAMDisplay, ('POINTS', 'U', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
comFlow5FineOpenFOAMDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
comFlow5FineOpenFOAMDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=comFlow5FineOpenFOAM,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine1.Source.Point1 = [0.0, 0.0, 2.2731382748331086e-15]
plotOverLine1.Source.Point2 = [0.4000263512134552, 0.4000263214111328, 0.30000001192092896]

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point1 = [0.0, 0.0, 0.02]
plotOverLine1.Source.Point2 = [0.05, 0.05, 0.02]

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point1 = [0.0, 0.0, 0.02]
plotOverLine1.Source.Point2 = [0.05, 0.05, 0.02]

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1)
# trace defaults for the display properties.
plotOverLine1Display.Representation = 'Surface'
plotOverLine1Display.ColorArrayName = ['POINTS', 'U']
plotOverLine1Display.LookupTable = uLUT
plotOverLine1Display.OSPRayScaleArray = 'U'
plotOverLine1Display.OSPRayScaleFunction = 'PiecewiseFunction'
plotOverLine1Display.SelectOrientationVectors = 'None'
plotOverLine1Display.ScaleFactor = 0.005000000074505806
plotOverLine1Display.SelectScaleArray = 'None'
plotOverLine1Display.GlyphType = 'Arrow'
plotOverLine1Display.GlyphTableIndexArray = 'None'
plotOverLine1Display.DataAxesGrid = 'GridAxesRepresentation'
plotOverLine1Display.PolarAxes = 'PolarAxesRepresentation'
plotOverLine1Display.GaussianRadius = 0.002500000037252903
plotOverLine1Display.SetScaleArray = ['POINTS', 'arc_length']
plotOverLine1Display.ScaleTransferFunction = 'PiecewiseFunction'
plotOverLine1Display.OpacityArray = ['POINTS', 'arc_length']
plotOverLine1Display.OpacityTransferFunction = 'PiecewiseFunction'

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')
lineChartView1.ViewSize = [490, 860]

# get layout
layout1 = GetLayout()

# place view in the layout
layout1.AssignView(2, lineChartView1)

# show data in view
plotOverLine1Display_1 = Show(plotOverLine1, lineChartView1)
# trace defaults for the display properties.
plotOverLine1Display_1.CompositeDataSetIndex = [0]
plotOverLine1Display_1.UseIndexForXAxis = 0
plotOverLine1Display_1.XArrayName = 'arc_length'
plotOverLine1Display_1.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine1Display_1.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.89', '0.1', '0.11', 'U_X', '0.22', '0.49', '0.72', 'U_Y', '0.3', '0.69', '0.29', 'U_Z', '0.6', '0.31', '0.64', 'U_Magnitude', '1', '0.5', '0', 'vtkValidPointMask', '0.65', '0.34', '0.16', 'Points_X', '0', '0', '0', 'Points_Y', '0.89', '0.1', '0.11', 'Points_Z', '0.22', '0.49', '0.72', 'Points_Magnitude', '0.3', '0.69', '0.29']
plotOverLine1Display_1.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine1Display_1.SeriesLabelPrefix = ''
plotOverLine1Display_1.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine1Display_1.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.2', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
plotOverLine1Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine1Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['U_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['U_Z', 'U_Magnitude']

# set active source
SetActiveSource(comFlow5FineOpenFOAM)

# create a new 'Plot Over Line'
plotOverLine2 = PlotOverLine(Input=comFlow5FineOpenFOAM,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine2.Source.Point1 = [0.0, 0.0, 2.2731382748331086e-15]
plotOverLine2.Source.Point2 = [0.4000263512134552, 0.4000263214111328, 0.30000001192092896]

# Properties modified on plotOverLine2.Source
plotOverLine2.Source.Point1 = [0.0, 0.0, 0.04]
plotOverLine2.Source.Point2 = [0.05, 0.05, 0.04]

# Properties modified on plotOverLine2
plotOverLine2.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine2.Source
plotOverLine2.Source.Point1 = [0.0, 0.0, 0.04]
plotOverLine2.Source.Point2 = [0.05, 0.05, 0.04]

# show data in view
plotOverLine2Display = Show(plotOverLine2, lineChartView1)
# trace defaults for the display properties.
plotOverLine2Display.CompositeDataSetIndex = [0]
plotOverLine2Display.UseIndexForXAxis = 0
plotOverLine2Display.XArrayName = 'arc_length'
plotOverLine2Display.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine2Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.89', '0.1', '0.11', 'U_X', '0.22', '0.49', '0.72', 'U_Y', '0.3', '0.69', '0.29', 'U_Z', '0.6', '0.31', '0.64', 'U_Magnitude', '1', '0.5', '0', 'vtkValidPointMask', '0.65', '0.34', '0.16', 'Points_X', '0', '0', '0', 'Points_Y', '0.89', '0.1', '0.11', 'Points_Z', '0.22', '0.49', '0.72', 'Points_Magnitude', '0.3', '0.69', '0.29']
plotOverLine2Display.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine2Display.SeriesLabelPrefix = ''
plotOverLine2Display.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine2Display.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine2Display.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.04', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
plotOverLine2Display.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine2Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine2Display.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine2Display.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z H0.04', 'U_Magnitude', 'U_Magnitude H0.04', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesVisibility = ['p', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesVisibility = ['U_Z', 'U_Magnitude']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '0.333333', '0', '1', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.333333', '0', '0.498039', 'U_Magnitude', '0.333333', '0', '1', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '2', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']

# set active source
SetActiveSource(plotOverLine1)

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0', '1', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.02', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z H0.02', 'U_Magnitude', 'U_Magnitude H0.02', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '2', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']

# set active source
SetActiveSource(comFlow5FineOpenFOAM)

# create a new 'Plot Over Line'
plotOverLine3 = PlotOverLine(Input=comFlow5FineOpenFOAM,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine3.Source.Point1 = [0.0, 0.0, 2.2731382748331086e-15]
plotOverLine3.Source.Point2 = [0.4000263512134552, 0.4000263214111328, 0.30000001192092896]

# set active source
SetActiveSource(plotOverLine1)

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '1', '0', '1', 'U_Magnitude', '1', '0', '1', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# set active source
SetActiveSource(plotOverLine3)

# set active source
SetActiveSource(plotOverLine2)

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.333333', '0', '1', 'U_Magnitude', '0.333333', '0', '1', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# set active source
SetActiveSource(plotOverLine3)

# Properties modified on plotOverLine3.Source
plotOverLine3.Source.Point1 = [0.0, 0.0, 0.06]
plotOverLine3.Source.Point2 = [0.05, 0.05, 0.06]

# Properties modified on plotOverLine3
plotOverLine3.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine3.Source
plotOverLine3.Source.Point1 = [0.0, 0.0, 0.06]
plotOverLine3.Source.Point2 = [0.05, 0.05, 0.06]

# show data in view
plotOverLine3Display = Show(plotOverLine3, lineChartView1)
# trace defaults for the display properties.
plotOverLine3Display.CompositeDataSetIndex = [0]
plotOverLine3Display.UseIndexForXAxis = 0
plotOverLine3Display.XArrayName = 'arc_length'
plotOverLine3Display.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine3Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.89', '0.1', '0.11', 'U_X', '0.22', '0.49', '0.72', 'U_Y', '0.3', '0.69', '0.29', 'U_Z', '0.6', '0.31', '0.64', 'U_Magnitude', '1', '0.5', '0', 'vtkValidPointMask', '0.65', '0.34', '0.16', 'Points_X', '0', '0', '0', 'Points_Y', '0.89', '0.1', '0.11', 'Points_Z', '0.22', '0.49', '0.72', 'Points_Magnitude', '0.3', '0.69', '0.29']
plotOverLine3Display.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine3Display.SeriesLabelPrefix = ''
plotOverLine3Display.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine3Display.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine3Display.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.06', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
plotOverLine3Display.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine3Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine3Display.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine3Display.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z H0.06', 'U_Magnitude', 'U_Magnitude H0.06', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesVisibility = ['p', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesVisibility = ['U_Z', 'U_Magnitude']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.501961', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '1', '0.666667', '0', 'U_Magnitude', '1', '0.501961', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '1', '0.501961', '0', 'U_Magnitude', '1', '0.501961', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine3Display
plotOverLine3Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '2', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']

# set active source
SetActiveSource(comFlow5FineOpenFOAM)

# create a new 'Plot Over Line'
plotOverLine4 = PlotOverLine(Input=comFlow5FineOpenFOAM,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine4.Source.Point1 = [0.0, 0.0, 2.2731382748331086e-15]
plotOverLine4.Source.Point2 = [0.4000263512134552, 0.4000263214111328, 0.30000001192092896]

# Properties modified on plotOverLine4.Source
plotOverLine4.Source.Point1 = [0.0, 0.0, 0.08]
plotOverLine4.Source.Point2 = [0.05, 0.05, 0.08]

# Properties modified on plotOverLine4
plotOverLine4.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine4.Source
plotOverLine4.Source.Point1 = [0.0, 0.0, 0.08]
plotOverLine4.Source.Point2 = [0.05, 0.05, 0.08]

# show data in view
plotOverLine4Display = Show(plotOverLine4, lineChartView1)
# trace defaults for the display properties.
plotOverLine4Display.CompositeDataSetIndex = [0]
plotOverLine4Display.UseIndexForXAxis = 0
plotOverLine4Display.XArrayName = 'arc_length'
plotOverLine4Display.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine4Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine4Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.89', '0.1', '0.11', 'U_X', '0.22', '0.49', '0.72', 'U_Y', '0.3', '0.69', '0.29', 'U_Z', '0.6', '0.31', '0.64', 'U_Magnitude', '1', '0.5', '0', 'vtkValidPointMask', '0.65', '0.34', '0.16', 'Points_X', '0', '0', '0', 'Points_Y', '0.89', '0.1', '0.11', 'Points_Z', '0.22', '0.49', '0.72', 'Points_Magnitude', '0.3', '0.69', '0.29']
plotOverLine4Display.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine4Display.SeriesLabelPrefix = ''
plotOverLine4Display.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine4Display.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine4Display.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.08', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine4Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
plotOverLine4Display.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine4Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine4Display.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine4Display.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z H0.08', 'U_Magnitude', 'U_Magnitude H0.08', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '0.333333', '0.666667', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.333333', '0.666667', '0', 'U_Magnitude', '0.333333', '0.666667', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesVisibility = ['p', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesVisibility = ['p', 'U_Z', 'U_Magnitude', 'vtkValidPointMask']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesVisibility = ['U_Z', 'U_Magnitude', 'vtkValidPointMask']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesVisibility = ['U_Z', 'U_Magnitude']

# Properties modified on plotOverLine4Display
plotOverLine4Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '2', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']

# set active source
SetActiveSource(comFlow5FineOpenFOAM)

# create a new 'Plot Data'
plotData1 = PlotData(Input=comFlow5FineOpenFOAM)

# set active source
SetActiveSource(comFlow5FineOpenFOAM)

# destroy plotData1
Delete(plotData1)
del plotData1

# create a new 'Plot Over Line'
plotOverLine5 = PlotOverLine(Input=comFlow5FineOpenFOAM,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine5.Source.Point1 = [0.0, 0.0, 2.2731382748331086e-15]
plotOverLine5.Source.Point2 = [0.4000263512134552, 0.4000263214111328, 0.30000001192092896]

# Properties modified on plotOverLine5.Source
plotOverLine5.Source.Point1 = [0.0, 0.0, 0.1]
plotOverLine5.Source.Point2 = [0.05, 0.05, 0.1]

# Properties modified on plotOverLine5
plotOverLine5.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine5.Source
plotOverLine5.Source.Point1 = [0.0, 0.0, 0.1]
plotOverLine5.Source.Point2 = [0.05, 0.05, 0.1]

# show data in view
plotOverLine5Display = Show(plotOverLine5, lineChartView1)
# trace defaults for the display properties.
plotOverLine5Display.CompositeDataSetIndex = [0]
plotOverLine5Display.UseIndexForXAxis = 0
plotOverLine5Display.XArrayName = 'arc_length'
plotOverLine5Display.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine5Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine5Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.89', '0.1', '0.11', 'U_X', '0.22', '0.49', '0.72', 'U_Y', '0.3', '0.69', '0.29', 'U_Z', '0.6', '0.31', '0.64', 'U_Magnitude', '1', '0.5', '0', 'vtkValidPointMask', '0.65', '0.34', '0.16', 'Points_X', '0', '0', '0', 'Points_Y', '0.89', '0.1', '0.11', 'Points_Z', '0.22', '0.49', '0.72', 'Points_Magnitude', '0.3', '0.69', '0.29']
plotOverLine5Display.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine5Display.SeriesLabelPrefix = ''
plotOverLine5Display.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine5Display.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine5Display.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude H0.10', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine5Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
plotOverLine5Display.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine5Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine5Display.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine5Display.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z H0.10', 'U_Magnitude', 'U_Magnitude H0.10', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesVisibility = ['p', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesVisibility = ['U_Z', 'U_Magnitude']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '0.6', '0.310002', '0.639994', 'U_Magnitude', '1', '0', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.889998', '0.100008', '0.110002', 'U_X', '0.220005', '0.489998', '0.719997', 'U_Y', '0.300008', '0.689998', '0.289998', 'U_Z', '1', '0', '0', 'U_Magnitude', '1', '0', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']

# Properties modified on plotOverLine5Display
plotOverLine5Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '2', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']

# set active view
SetActiveView(renderView1)

# set active view
SetActiveView(lineChartView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.06874655823144328, -0.8584346753247059, 0.7767019910128812]
renderView1.CameraFocalPoint = [0.20001317560672774, 0.20001316070556635, 0.15000000596046553]
renderView1.CameraViewUp = [0.011997532388685853, 0.5083468847152827, 0.8610688149136801]
renderView1.CameraParallelScale = 0.32017266694684826

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).