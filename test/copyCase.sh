############################################################
#  Filename: 	copyCase.sh
#  purpose:  	Create a copy of the relevant of a case to  
#	       	a new case
############################################################

destination="./../$1"
if [ $# -eq 1 ]; then
	if [ -d $destination ]; then
		echo "The directory already exists, choose another name."
	else 
		echo "Creating directory $destination"
		mkdir $destination
	# Copy the relevant folders:
		folders="$(find . -maxdepth 1 -type d | grep -v "[1-9].*" | grep -v "processor*" | grep -v "postProcessing" | grep "./")"
		extensions='.hdf .py .sh'
		for f in $folders; do
			echo "copying $f"			
			cp -r $f $destination			
		done
	#copy the scripts
		for g in $extensions; do
			No="$(find . -type f -name "*$g" | wc -l)"	#checks amount of .$g files
			if [ $No -ge 1 ]; then	
				cp -r *$g $destination
				echo "copied $g files"
			fi 
		done
	fi
else
	echo "The number of arguments is $# while it should be 1."
fi

