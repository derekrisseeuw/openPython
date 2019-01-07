#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
fluidfoam = FindSource('Fluid.foam')

# create a new 'Calculator'
calculator1 = Calculator(Input=fluidfoam)
calculator1.Function = ''

# find source
contour1 = FindSource('Contour1')

# Properties modified on calculator1
calculator1.Function = 'vorticity_Z*U_Z*0.05/0.04'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1482, 860]

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# show data in view
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['POINTS', 'Result']
calculator1Display.LookupTable = resultLUT
calculator1Display.OSPRayScaleArray = 'Result'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'U'
calculator1Display.ScaleFactor = 0.06000307798385621
calculator1Display.SelectScaleArray = 'Result'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'Result'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityFunction = resultPWF
calculator1Display.ScalarOpacityUnitDistance = 0.005586622735757563
calculator1Display.GaussianRadius = 0.030001538991928103
calculator1Display.SetScaleArray = ['POINTS', 'Result']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Result']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
calculator1Display.OSPRayScaleFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
calculator1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
calculator1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
calculator1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
calculator1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
calculator1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
calculator1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
calculator1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

# hide data in view
Hide(fluidfoam, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# Rescale transfer function
pLUT.RescaleTransferFunction(-0.799458622932, 0.168856099248)

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# Rescale transfer function
pPWF.RescaleTransferFunction(-0.799458622932, 0.168856099248)

# hide data in view
Hide(calculator1, renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.049135647775255906, 0.12610923715339223, 0.5110623606975309]
renderView1.CameraFocalPoint = [7.748603820800781e-07, -1.537799835205078e-05, 0.0]
renderView1.CameraViewUp = [-0.011373077929330337, 0.9710625829582414, -0.23855421412517921]
renderView1.CameraParallelScale = 0.5196245889200986

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).










slice with the z-vorticity
=============================================================
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
fluidfoam = FindSource('Fluid.foam')

# create a new 'Slice'
slice1 = Slice(Input=fluidfoam)

# find source
contour1 = FindSource('Contour1')

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.0, 0.0, -0.05]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.0, 0.0, -0.05]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1482, 860]

# show data in view
slice1Display = Show(slice1, renderView1)
# trace defaults for the display properties.
slice1Display.Representation = 'Surface'

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# find source
calculator1 = FindSource('Calculator1')

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'vorticity', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vorticity'
vorticityLUT = GetColorTransferFunction('vorticity')

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'vorticity', 'Z'))

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, False)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(vorticityLUT, slice1Display)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityLUT.ApplyPreset('Preset', True)

# get opacity transfer function/opacity map for 'vorticity'
vorticityPWF = GetOpacityTransferFunction('vorticity')

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityPWF.ApplyPreset('Preset', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityLUT.ApplyPreset('Preset', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityPWF.ApplyPreset('Preset', True)

# Properties modified on vorticityLUT
vorticityLUT.EnableOpacityMapping = 1

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityLUT.ApplyPreset('Preset 0', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityPWF.ApplyPreset('Preset 0', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityLUT.ApplyPreset('Preset 0', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
vorticityPWF.ApplyPreset('Preset 0', True)

# Rescale transfer function
vorticityLUT.RescaleTransferFunction(-3770.55151367, 1594.0447998)

# Rescale transfer function
vorticityPWF.RescaleTransferFunction(-3770.55151367, 1594.0447998)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# Rescale transfer function
vorticityLUT.RescaleTransferFunction(-1000.0, 1000.0)

# Rescale transfer function
vorticityPWF.RescaleTransferFunction(-1000.0, 1000.0)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.049135647775255906, 0.12610923715339223, 0.5110623606975309]
renderView1.CameraFocalPoint = [7.748603820800781e-07, -1.537799835205078e-05, 0.0]
renderView1.CameraViewUp = [-0.011373077929330337, 0.9710625829582414, -0.23855421412517921]
renderView1.CameraParallelScale = 0.5196245889200986

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
