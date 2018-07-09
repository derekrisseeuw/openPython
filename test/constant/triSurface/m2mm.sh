files='bottom nozzleHolder outer symmetryY symmetryX top nozzleInlet' # nozzleInlet exclude nozzleInlet??! 
scale=0.001
rot=0
for f in $files; do
	mv $f.stl $f.mm.stl
	surfaceTransformPoints -scale "($scale $scale $scale)" $f.mm.stl $f.stl
	if [ $rot -eq 1 ]; then		# rotate first around the x-axis and then the z-axis
		mv $f.stl $f.backup.stl
	        surfaceTransformPoints -rotate-angle "((1 0 0) 90)" $f.backup.stl $f.temp.stl	
		sleep 0.1
		surfaceTransformPoints -rotate-angle "((0 0 1) 90)" $f.temp.stl $f.stl
		rm $f.temp.stl
	fi
done

