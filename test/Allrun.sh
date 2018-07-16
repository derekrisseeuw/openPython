cd ${0%/*} || exit 1    		 # Run from this directory
. $WM_PROJECT_DIR/bin/tools/RunFunctions


./Allrun.sh.pre

solver=$(getApplication)	# Requires the application specified in controlDict
foamJob -w $solver
mv log $solver.log
