#!/bin/bash


rsphere=$1
rhole=$2
x=$3
y=$4
z=$5

compr=0.00

python copysilica.py so2.xyz $x $y $z
python centralizexyz.py silicacopy_out.xyz
python digahole.py silicacopy_out_centralized.xyz $rhole
python fccsphere.py $rsphere 40 $compr
python combinexyz.py holesomelattice.xyz fccsphere.xyz
