set logscale y
set title "Time step"
set ylabel 'delta T'
set xlabel 'Iteration'
plot "< cat log | grep 'deltaT' | cut -d' ' -f3" title 'deltaT' with lines
pause 1
reread
