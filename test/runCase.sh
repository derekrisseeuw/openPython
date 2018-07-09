#!/bin/sh
cd ${0%/*} || exit 1    		    # Run from this directory
. $WM_PROJECT_DIR/bin/tools/RunFunctions    # Tutorial run functions

#------------------------------ USER INPUT SECTION -----------------------------#
# check what parts of the code to run.
#    	MESHING
block=1			# blockMesh. 			Requires blockMeshDict
decompose1=0		# decompose previous to .. 	Requires decomposeParDict  
snappy=0		# snappyHexMesh. 		Requires snappyHexMeshDict
extrude=1		#extrude the mesh

# 	RUNNING AND POSTPROCESSING
prepareCase=1		# create 0-folder with initial conditions
decompose2=1		# Decompose the case		Requires decomposeParDict 
potential=0		# Create initial field 		Requires 'potentialFlow' in fvSolution
run=1			# Run the case with $solver	Requires controlDict
foamToVTK=0
reconstruct=0		# Reconstruct the parallel case
postProcess=0		# Open paraview with paraview	
#------------------------------------------------------------------------------#

solver=$(getApplication)	# Requires the application specified in controlDict
np=$(getNumberOfProcessors)	# number of processors

string="\n---------------------------------------\n"

#------------------------------ MESHING PART -----------------------------------#
#BLOCKMESH
if [ $block -eq 1 ]; then
	rm *.log			 # clean the case of additional logfiles
	rm -r 0
	mkdir 0
	foamJob -w blockMesh
	mv log blockMesh.log
	echo "$string blockMesh has run $string"
fi

#DECOMPOSE
if [ $decompose1 -eq 1 ]; then
	foamJob -w decomposePar -force 
	mv log decompose1.log
	echo "$string Mesh is decomposed $string"
	parMesh=1				# parallel meshing is true
else
	parMesh=0
fi

#Snappyhexmesh and reconstruct
if [ $snappy -eq 1 ]; then
	foamJob -w surfaceFeatureExtract
	mv log surfaceFeatureExtract.log
	if [ $parMesh -eq 1 ]; then
  		foamJob -p -w snappyHexMesh -overwrite
		mv log snappyHexMesh.log
		echo "$string snappyHexMesh has run in parallel $string"
		foamJob -w reconstructParMesh -constant
		mv log reconstructParMesh.log
		echo "$string reconstructParMesh has run $string"
		rm -r processor*
	else
		foamJob -w snappyHexMesh -overwrite
		mv log snappyHexMesh.log
		echo "$string snappyHexMesh has run in serial $string"
	fi

	#Run checkMesh	
	foamJob -w checkMesh			# check the mesh quality
	mv log checkMesh.log
	check="$(cat checkMesh.log | grep Failed | wc -l)"	
	if [ $check -ge 1 ]; then
		echo "$sting The mesh quality is poor, check the checkMesh.log file $string"
	fi

	## ADAPT BOUNDARY FILE FOR NEW MESH
	echo $string
	echo '1. Edit the constant/polymesh/boundary file and remove all the references to patches created by blockMesh;'
	echo 'Leave only the patches desired for the simulation to run. Edit the number at the top of the text file which shows how many patches are to be setup.'
	echo "$sting continuing run... $string"
fi


if [ $extrude -eq 1 ]; then
	foamJob -w extrudeMesh
	mv log extrudeMesh.log
	foamJob -w changeDictionary
	foamJob -w createPatch -overwrite
	echo "$string extrudeMesh has run $string"
	rm log
fi


#------------------------------ SOLVER PART -----------------------------------#
#PREPARE THE BOUNDARY CONDITIONS
if [ $prepareCase -eq 1 ]; then
	rm -r 0
	cp -r 0.orig 0
	echo "$string case initial conditions have been prepared $string"
fi


#Decompose updated mesh
if [ $decompose2 -eq 1 ]; then
	foamJob -w decomposePar -force 
	mv log decompose2.log
	foamJob -p -w renumberMesh -overwrite 
	mv log renumberMesh.log
	echo "$string Decomposed case has been prepared $string"
	parallel=1
else
	parallel=0
fi

#SOLVER
if [ $run -eq 1 ]; then
	if [ $parallel -eq 1 ]; then
		if [ $potential -eq 1 ]; then
			foamJob -w -p potentialFoam
			mv log potentialFoam.log
		fi
		echo "$string $solver is running in parallel mode $string"
  		foamJob -p -w $solver
		mv log $solver.log

	else
		if [ $potential -eq 1 ]; then
			foamJob -w potentialFoam
			mv log potentialFoam.log
		fi
		echo "$string $solver is running in serial mode $string"
		foamJob -w $solver
		mv log $solver.log
	fi
	echo "$string $solver has finished run $string"
fi

#VTK result for postprocessing
if [ $foamToVTK -eq 1 ]; then
	foamJob -w -p foamToVTK 
	mv log foamToVTK.log
	echo "$string Case has been reconstructed $string"
fi

#Reconstruct mesh
if [ $reconstruct -eq 1 ]; then
	foamJob -w reconstructPar -withZero
	mv log reconstruct.log
	echo "$string Case has been reconstructed $string"
fi

#START PARAFOAM
if [ $postProcess -eq 1 ]; then
	touch case.foam
  	paraview --mpi case.foam
fi
