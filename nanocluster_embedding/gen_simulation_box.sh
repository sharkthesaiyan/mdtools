#!/bin/bash

scriptpath=/home/local/vejantun/Programs/mdtools/nanocluster_embedding
goldfile=$1
if [ $# == "4" ]; then
	x=$3
	y=$4
	z=$5
else
	x=2
	y=2
	z=4
fi

python $scriptpath/copysilica.py $x $y $z
python $scriptpath/centralizexyz.py silicacopy_out.xyz
ovitos $scriptpath/ovitos_get_surface.py $goldfile
python $scriptpath/hole_to_silica.py $goldfile silicacopy_out_centralized.xyz surface.vtk 1.0
python $scriptpath/combinexyz.py holedsilicaout.xyz $goldfile
rm silicacopy_out.xyz
rm silicacopy_out_centralized.xyz
rm surface.vtk
rm holedsilicaout.xyz
