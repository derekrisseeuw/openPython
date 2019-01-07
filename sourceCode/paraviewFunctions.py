
#### import the simple module from the paraview
from paraview.simple import *
import os
import numpy as np

def paraviewContour(fluidfoam, renderView, plotSetting):
	""" 
	Function to create a new contour in the plot with a solid colour and opacity
	"""
	# create a new 'Contour'
	#extract the plotSettings
	parameter 	= plotSetting['parameter']
	level		= plotSetting['level']
	colour 		= list(plotSetting['colour'])
	opacity 	= plotSetting['opacity']

	contour1 = Contour(Input=fluidfoam)
	contour1.ContourBy = ['POINTS', parameter]
	contour1.Isosurfaces = [level]
	contour1.PointMergeMethod = 'Uniform Binning'

	# show data in view
	contour1Display = Show(contour1, renderView)
	# trace defaults for the display properties.
	contour1Display.Representation = 'Surface'
	contour1Display.ColorArrayName = [None, '']
	contour1Display.OSPRayScaleArray = 'Normals'
	contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	contour1Display.SelectOrientationVectors = 'None'
	contour1Display.ScaleFactor = 0.010506926476955414
	contour1Display.SelectScaleArray = 'None'
	contour1Display.GlyphType = 'Arrow'
	contour1Display.GlyphTableIndexArray = 'None'
	contour1Display.DataAxesGrid = 'GridAxesRepresentation'
	contour1Display.PolarAxes = 'PolarAxesRepresentation'
	contour1Display.GaussianRadius = 0.005253463238477707
	contour1Display.SetScaleArray = [None, '']
	contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
	contour1Display.OpacityArray = [None, '']
	contour1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
	contour1Display.OSPRayScaleFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

	# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
	contour1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
	contour1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
	contour1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
	contour1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
	contour1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
	contour1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

	# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
	contour1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
	contour1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
	contour1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
	contour1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

	# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
	contour1Display.ScaleTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]
	# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
	contour1Display.OpacityTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

	# hide data in view
	Hide(fluidfoam, renderView)

	# update the view to ensure updated data information
	renderView.Update()
	contour1Display.DiffuseColor = colour; 
	contour1Display.Opacity = opacity

	#### saving camera placements for all active views
	return contour1

def simpleAddition(num):
	return num+1

def helicalDensityZ(fluidfoam, name):
	"""
	Compute the scaled helical density from the z-vorticity and the z-U 
	"""
	calculator1 = Calculator(Input=fluidfoam)
	calculator1.ResultArrayName= name
	calculator1.Function = 'vorticity_Z*U_Z*0.05/0.04'
	return calculator1

def scaledPressure(fluidfoam):
	"""
	Compute the scaled helical density from the z-vorticity and the z-U 
	"""
	calculator1 = Calculator(Input=fluidfoam)
	calculator1.ResultArrayName = 'scaledPressure'
	calculator1.Function = 'p*1000'
	return calculator1

def paraviewSlice(fluidfoam, renderView, plotSetting):
	""" 
	Function to create a new slice in the plot for a parameter with a colourmap
	"""
	# create a new 'Contour'
	#extract the plotSettings
	parameter 	= plotSetting['parameter']
	location 	= plotSetting['location']
	colour 		= plotSetting['colour']
	colourRange = plotSetting['colourRange']

	# create a new 'Slice'
	slice1 = Slice(Input=fluidfoam)

	print()
	print('location = ' + str(location))
	# Properties modified on slice1.SliceType
	slice1.SliceType.Origin = location[0]
	slice1.SliceType.Normal = location[1]

	# show data in view
	slice1Display = Show(slice1, renderView)
	# trace defaults for the display properties.
	slice1Display.Representation = 'Surface'

	# get color transfer function/color map for 'p'
	pLUT = GetColorTransferFunction('p')

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(pLUT, renderView)

	# rescale color and/or opacity maps used to include current data range
	slice1Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice1Display.SetScalarBarVisibility(renderView, False)

	# get color transfer function/color map for parameter
	vorticityLUT = GetColorTransferFunction(parameter)

	# set scalar coloring
	ColorBy(slice1Display, ('POINTS', parameter, 'Z'))

	# rescale color and/or opacity maps used to exactly fit the current data range
	slice1Display.RescaleTransferFunctionToDataRange(False, False)

	# Update a scalar bar component title.
	UpdateScalarBarsComponentTitle(vorticityLUT, slice1Display)

	# get opacity transfer function/opacity map for 'vorticity'
	vorticityPWF = GetOpacityTransferFunction('vorticity')

	# Properties modified on vorticityLUT
	vorticityLUT.EnableOpacityMapping = 1

	# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
	vorticityLUT.ApplyPreset(colour, True)

	# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
	vorticityPWF.ApplyPreset(colour, True)

	# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
	vorticityLUT.ApplyPreset(colour, True)

	# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
	vorticityPWF.ApplyPreset(colour, True)

	# Rescale transfer function
	vorticityPWF.RescaleTransferFunction(colourRange[0], colourRange[1])

	# update the view to ensure updated data information
	renderView.Update()

	return slice1

def reflect(fluidfoam, renderview):
	# create a new 'Reflect'
	reflect1 = Reflect(Input=fluidfoam)

	# Properties modified on reflect1
	reflect1.Plane = 'Z Max'

	# get active view
	renderView = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView.ViewSize = [1164, 860]

	# get color transfer function/color map for 'p'
	pLUT = GetColorTransferFunction('p')

	# get opacity transfer function/opacity map for 'p'
	pPWF = GetOpacityTransferFunction('p')

	# show data in view
	reflect1Display = Show(reflect1, renderView)
	# trace defaults for the display properties.
	reflect1Display.Representation = 'Surface'
	reflect1Display.ColorArrayName = ['POINTS', 'p']
	reflect1Display.LookupTable = pLUT
	reflect1Display.OSPRayScaleArray = 'p'
	reflect1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	reflect1Display.SelectOrientationVectors = 'U'
	reflect1Display.ScaleFactor = 0.0800015926361084
	reflect1Display.SelectScaleArray = 'p'
	reflect1Display.GlyphType = 'Arrow'
	reflect1Display.GlyphTableIndexArray = 'p'
	reflect1Display.DataAxesGrid = 'GridAxesRepresentation'
	reflect1Display.PolarAxes = 'PolarAxesRepresentation'
	reflect1Display.ScalarOpacityFunction = pPWF
	reflect1Display.ScalarOpacityUnitDistance = 0.008235934505434316
	reflect1Display.GaussianRadius = 0.0400007963180542
	reflect1Display.SetScaleArray = ['POINTS', 'p']
	reflect1Display.ScaleTransferFunction = 'PiecewiseFunction'
	reflect1Display.OpacityArray = ['POINTS', 'p']
	reflect1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
	reflect1Display.OSPRayScaleFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

	# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
	reflect1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
	reflect1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
	reflect1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
	reflect1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
	reflect1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
	reflect1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

	# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
	reflect1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
	reflect1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
	reflect1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
	reflect1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

	# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
	reflect1Display.ScaleTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

	# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
	reflect1Display.OpacityTransferFunction.Points = [0.0, 0.02631578966975212, 0.5, 0.0, 480.0, 1.0, 0.5, 0.0]

	# hide data in view
	Hide(fluidfoam, renderView)

	# show color bar/color legend
	# reflect1Display.SetScalarBarVisibility(renderView, True)

	# update the view to ensure updated data information
	renderView.Update()

	# reflect1Display.DiffuseColor = [0.6666666666666666, 0.6666666666666666, 1.0]
	reflect1Display.Opacity = 1.

	return reflect1