#!/bin/bash
gnuplot -persist <<-EOFMarker
load "neutrino-luminosity.cfg";
set term png;
set output "file.png";
plot "NeutrinoLuminosity.dat" u (\$1)*time_geo_mks:(@col2) w l ls 1
EOFMarker
