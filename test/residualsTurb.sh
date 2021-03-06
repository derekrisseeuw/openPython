set logscale y
set title "Residuals"
set ylabel 'Residual'
set xlabel 'Iteration'
plot "< cat log | grep 'Solving for Ux' | cut -d' ' -f9" title 'Ux' with lines,\
"< cat log | grep 'Solving for omega' | cut -d' ' -f9" title 'omega' with lines,\
"< cat log | grep 'Solving for k' | cut -d' ' -f9" title 'k' with lines,\
"< cat log | grep 'Solving for p' | cut -d' ' -f9" title 'p' with lines
pause 1
reread
