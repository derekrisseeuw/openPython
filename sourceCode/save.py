
#### import the simple module from the paraview
from paraview.simple import *
import os
import numpy as np

def paraviewContour(Input, renderview, plotSetting):
	""" 
	Function to create a new contour in the plot with a solid colour and opacity
	"""
	# create a new 'Contour'
	#extract the plotSettings
	parameter 	= plotSetting['parameter']
	level		= plotSetting['level']
	colour 		= plotSetting['colour']
	opacity 	= plotSetting['opacity']

	contour1 = Contour(Input=fluidfoam)
	contour1.ContourBy = ['POINTS', parameter]
	contour1.Isosurfaces = [level]
	contour1.PointMergeMethod = 'Uniform Binning'

	# show data in view
	contour1Display = Show(contour1, renderView1)
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
	Hide(fluidfoam, renderView1)

	# update the view to ensure updated data information
	renderView1.Update()
	contour1Display.DiffuseColor = colour; 
	contour1Display.Opacity = opacity

	#### saving camera placements for all active views
	return contour1