############################################################
#  Filename: cleanCase
#  purpose:  Clean the time folders in the present case. 
#
###########################################################

parallel=0
serial=0
echo "Cleaning $PWD case"
#check what parts of the code to run
if [ -d "processor0" ]; then
	if [ -d "0" ]; then
		read -p "clean Parallel (1) or serial (2) case, or both (3):" input
		echo $input
		if  [[ $input -eq 1 ]]; then
			parallel=1
		elif [[ $input -eq 2 ]]; then 
			serial=1
		else
			parallel=1
			serial=1
		fi
	else
		parallel=1
	fi		
else
	serial=1
fi

#Delete the files
if [[ $parallel -eq 1 ]];then 
  	for f in processor*
		do rm -rf ./$f/[1-9]* ./$f/0.* >/dev/null 2>&1
  	done
	echo "parallel case is cleaned"
fi
if [[ $serial -eq 1 ]];then
	rm -rf ./[1-9]* ./0.[0-9]* >/dev/null 2>&1
	echo "serial case is cleaned"
fi
rm -r postProcessing
