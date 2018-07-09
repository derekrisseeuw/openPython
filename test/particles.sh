#set logscale y
set title "Time step"
set ylabel 'Number of particles'
set xlabel 'Iteration'
plot "< cat sprayFoam.log | grep 'Current number' | cut -d' ' -f16" title 'Number of Particles' with lines
pause 1
reread
