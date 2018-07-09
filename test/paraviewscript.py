#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
shieldFlow2OpenFOAM = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1404, 860]

# get display properties
shieldFlow2OpenFOAMDisplay = GetDisplayProperties(shieldFlow2OpenFOAM, view=renderView1)

# Properties modified on shieldFlow2OpenFOAMDisplay
shieldFlow2OpenFOAMDisplay.Opacity = 0.0

# Properties modified on shieldFlow2OpenFOAMDisplay
shieldFlow2OpenFOAMDisplay.Opacity = 0.3

# Properties modified on shieldFlow2OpenFOAM
shieldFlow2OpenFOAM.VolumeFields = ['T', 'k', 'nut', 'omega', 'p', 'rho', 'U']

# update the view to ensure updated data information
renderView1.Update()

# create a new 'PVFoamReader'
shieldFlow2OpenFOAM_1 = PVFoamReader(FileName='/media/qlayerspc/DATA/Linux/OpenFOAM/run/spray/shieldFlow/shieldFlow2/shieldFlow2.OpenFOAM')
shieldFlow2OpenFOAM_1.MeshParts = ['internalMesh']
shieldFlow2OpenFOAM_1.VolumeFields = ['p', 'U']
shieldFlow2OpenFOAM_1.LagrangianFields = []

# Properties modified on shieldFlow2OpenFOAM_1
shieldFlow2OpenFOAM_1.MeshParts = ['lagrangian/sprayCloud']
shieldFlow2OpenFOAM_1.LagrangianFields = ['d', 'mass0', 'U']

# show data in view
shieldFlow2OpenFOAM_1Display = Show(shieldFlow2OpenFOAM_1, renderView1)
# trace defaults for the display properties.
shieldFlow2OpenFOAM_1Display.Representation = 'Surface'
shieldFlow2OpenFOAM_1Display.ColorArrayName = [None, '']
shieldFlow2OpenFOAM_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
shieldFlow2OpenFOAM_1Display.SelectOrientationVectors = 'None'
shieldFlow2OpenFOAM_1Display.ScaleFactor = -2.0000000000000002e+298
shieldFlow2OpenFOAM_1Display.SelectScaleArray = 'None'
shieldFlow2OpenFOAM_1Display.GlyphType = 'Arrow'
shieldFlow2OpenFOAM_1Display.GlyphTableIndexArray = 'None'
shieldFlow2OpenFOAM_1Display.DataAxesGrid = 'GridAxesRepresentation'
shieldFlow2OpenFOAM_1Display.PolarAxes = 'PolarAxesRepresentation'
shieldFlow2OpenFOAM_1Display.GaussianRadius = -1.0000000000000001e+298
shieldFlow2OpenFOAM_1Display.SetScaleArray = [None, '']
shieldFlow2OpenFOAM_1Display.ScaleTransferFunction = 'PiecewiseFunction'
shieldFlow2OpenFOAM_1Display.OpacityArray = [None, '']
shieldFlow2OpenFOAM_1Display.OpacityTransferFunction = 'PiecewiseFunction'

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(shieldFlow2OpenFOAM)

# set scalar coloring
ColorBy(shieldFlow2OpenFOAMDisplay, ('POINTS', 'U', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
shieldFlow2OpenFOAMDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
shieldFlow2OpenFOAMDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# set active source
SetActiveSource(shieldFlow2OpenFOAM_1)

# create a new 'Glyph'
glyph1 = Glyph(Input=shieldFlow2OpenFOAM_1,
    GlyphType='Arrow')
glyph1.Scalars = ['POINTS', 'None']
glyph1.Vectors = ['POINTS', 'None']
glyph1.ScaleFactor = -2.0000000000000002e+298
glyph1.GlyphTransform = 'Transform2'

# set active source
SetActiveSource(shieldFlow2OpenFOAM_1)

# Properties modified on glyph1
glyph1.GlyphType = 'Sphere'
glyph1.ScaleFactor = -2e+298

# show data in view
glyph1Display = Show(glyph1, renderView1)
# trace defaults for the display properties.
glyph1Display.Representation = 'Surface'
glyph1Display.ColorArrayName = [None, '']
glyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
glyph1Display.SelectOrientationVectors = 'None'
glyph1Display.ScaleFactor = -2.0000000000000002e+298
glyph1Display.SelectScaleArray = 'None'
glyph1Display.GlyphType = 'Arrow'
glyph1Display.GlyphTableIndexArray = 'None'
glyph1Display.DataAxesGrid = 'GridAxesRepresentation'
glyph1Display.PolarAxes = 'PolarAxesRepresentation'
glyph1Display.GaussianRadius = -1.0000000000000001e+298
glyph1Display.SetScaleArray = [None, '']
glyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
glyph1Display.OpacityArray = [None, '']
glyph1Display.OpacityTransferFunction = 'PiecewiseFunction'

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
uLUT.RescaleTransferFunction(0.000180850780453, 8.34863571163)

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# Rescale transfer function
uPWF.RescaleTransferFunction(0.000180850780453, 8.34863571163)

# set active source
SetActiveSource(glyph1)

# set active source
SetActiveSource(shieldFlow2OpenFOAM_1)

# Properties modified on shieldFlow2OpenFOAM_1
shieldFlow2OpenFOAM_1.VolumeFields = []

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(glyph1)

# set active source
SetActiveSource(shieldFlow2OpenFOAM_1)

# Properties modified on shieldFlow2OpenFOAM_1Display
shieldFlow2OpenFOAM_1Display.SetScaleArray = [None, 'd']

# Properties modified on shieldFlow2OpenFOAM_1Display
shieldFlow2OpenFOAM_1Display.OpacityArray = [None, 'd']

# Properties modified on shieldFlow2OpenFOAM_1Display
shieldFlow2OpenFOAM_1Display.OSPRayScaleArray = 'U'

# set active source
SetActiveSource(glyph1)

# set scalar coloring
ColorBy(glyph1Display, ('POINTS', 'd'))

# rescale color and/or opacity maps used to include current data range
glyph1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
glyph1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'd'
dLUT = GetColorTransferFunction('d')

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# Properties modified on glyph1
glyph1.Scalars = ['POINTS', 'd']
glyph1.Vectors = ['POINTS', 'U']
glyph1.ScaleMode = 'scalar'
glyph1.ScaleFactor = 30.0

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
uLUT.RescaleTransferFunction(0.000180850780453, 8.36966561939)

# Rescale transfer function
uPWF.RescaleTransferFunction(0.000180850780453, 8.36966561939)

# Properties modified on glyph1Display
glyph1Display.OSPRayScaleArray = 'Normals'

# get color legend/bar for dLUT in view renderView1
dLUTColorBar = GetScalarBar(dLUT, renderView1)

# Properties modified on dLUTColorBar
dLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
dLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# set active source
SetActiveSource(shieldFlow2OpenFOAM)

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)

# Properties modified on uLUTColorBar
uLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
uLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# Properties modified on shieldFlow2OpenFOAMDisplay.DataAxesGrid
shieldFlow2OpenFOAMDisplay.DataAxesGrid.GridAxesVisibility = 1

# Properties modified on shieldFlow2OpenFOAMDisplay.DataAxesGrid
shieldFlow2OpenFOAMDisplay.DataAxesGrid.GridAxesVisibility = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 0

# Properties modified on renderView1
renderView1.CenterAxesVisibility = 1

# Properties modified on renderView1
renderView1.CenterAxesVisibility = 0

# Properties modified on renderView1
renderView1.HiddenLineRemoval = 1

# Properties modified on renderView1
renderView1.HiddenLineRemoval = 0

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 1

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.GoToLast()

# current camera placement for renderView1
renderView1.CameraPosition = [-0.05901090048468274, 0.21029861435473945, 0.2807098896483444]
renderView1.CameraFocalPoint = [0.07216503220857105, 0.07503249314102112, -0.0013010519613839973]
renderView1.CameraViewUp = [0.13628002587888324, 0.9164649611464932, -0.3761910811505341]
renderView1.CameraParallelScale = 0.10621726805409956

# save screenshot
SaveScreenshot('/media/qlayerspc/DATA/Linux/OpenFOAM/run/spray/shieldFlow/shieldFlow2/image_1234.png', renderView1, ImageResolution=[1008, 860])

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-0.05901090048468274, 0.21029861435473945, 0.2807098896483444]
renderView1.CameraFocalPoint = [0.07216503220857105, 0.07503249314102112, -0.0013010519613839973]
renderView1.CameraViewUp = [0.13628002587888324, 0.9164649611464932, -0.3761910811505341]
renderView1.CameraParallelScale = 0.10621726805409956

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).