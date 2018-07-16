#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(FileName='/media/qlayerspc/DATA/Linux/OpenFOAM/run/python/test/case.foam')
casefoam.MeshRegions = ['internalMesh']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [928, 860]

# show data in view
casefoamDisplay = Show(casefoam, renderView1)
# trace defaults for the display properties.
casefoamDisplay.Representation = 'Surface'
casefoamDisplay.ColorArrayName = [None, '']
casefoamDisplay.OSPRayScaleArray = 'CasePath'
casefoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
casefoamDisplay.SelectOrientationVectors = 'None'
casefoamDisplay.ScaleFactor = 0.015000000596046448
casefoamDisplay.SelectScaleArray = 'None'
casefoamDisplay.GlyphType = 'Arrow'
casefoamDisplay.GlyphTableIndexArray = 'None'
casefoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
casefoamDisplay.PolarAxes = 'PolarAxesRepresentation'
casefoamDisplay.ScalarOpacityUnitDistance = 0.011099901290376357
casefoamDisplay.GaussianRadius = 0.007500000298023224
casefoamDisplay.SetScaleArray = [None, '']
casefoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
casefoamDisplay.OpacityArray = [None, '']
casefoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(casefoamDisplay, ('CELLS', 'vtkCompositeIndex'))

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkCompositeIndex'
vtkCompositeIndexLUT = GetColorTransferFunction('vtkCompositeIndex')

# set scalar coloring
ColorBy(casefoamDisplay, ('FIELD', 'CasePath'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkCompositeIndexLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'CasePath'
casePathLUT = GetColorTransferFunction('CasePath')

# set scalar coloring
ColorBy(casefoamDisplay, ('CELLS', 'vtkCompositeIndex'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(casePathLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# Properties modified on casefoam
casefoam.SkipZeroTime = 0

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(casefoamDisplay, ('POINTS', 'vorticity', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkCompositeIndexLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vorticity'
vorticityLUT = GetColorTransferFunction('vorticity')

# Properties modified on casefoam
casefoam.CellArrays = ['U']

# update the view to ensure updated data information
renderView1.Update()

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vorticityLUT, renderView1)

# set scalar coloring
ColorBy(casefoamDisplay, ('CELLS', 'vtkCompositeIndex'))

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# current camera placement for renderView1
renderView1.CameraPosition = [0.011164919350949883, 0.16669076486363665, 0.32028605131617666]
renderView1.CameraFocalPoint = [0.075435227184386, 0.07057086407858501, 0.0014373218882190563]
renderView1.CameraViewUp = [0.022272531823500395, 0.958435182905113, -0.28443968516332957]
renderView1.CameraParallelScale = 0.10621726805409956

# save screenshot
SaveScreenshot('/media/qlayerspc/DATA/Linux/OpenFOAM/run/python/test/picture.png', renderView1, ImageResolution=[928, 860])

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.011164919350949883, 0.16669076486363665, 0.32028605131617666]
renderView1.CameraFocalPoint = [0.075435227184386, 0.07057086407858501, 0.0014373218882190563]
renderView1.CameraViewUp = [0.022272531823500395, 0.958435182905113, -0.28443968516332957]
renderView1.CameraParallelScale = 0.10621726805409956

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).