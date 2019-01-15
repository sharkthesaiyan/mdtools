#!/usr/bin/python

import sys
import numpy as np
import pointsinside
import recrystal as rec
import xyzio

def add_to_size_and_anticompress(points, emptySpace, compression=1.0, direction=0):
	#When making a cavity with even distance after the particle has decompressed to natural state
	#it's good to take care of the compression level here
	points = np.asarray(points)
	if(compression>0.0):
		points = points*(1.0/compression)
	else:
		print "no anticompression done in scale_to_and_anticompress (value error)"	

	#There shoudn't be zero values here unless you are doing something very weird
	points = [ p + emptySpace*p/np.linalg.norm(p) for p in points]
	return points

def main():
	goldFile = sys.argv[1]
	silicaFile = sys.argv[2]
	meshfile=sys.argv[3]
	emptySpace = float(sys.argv[4])
	#if(len(sys.argv)==8):	

	coord, header = xyzio.readxyz(silicaFile)
	coord = np.asarray([[a[0],a[1],a[2],a[3]] for a in coord])

	#print coord[0,:]

	#Silica to be included
	points, triangles = rec.read_vtk(meshfile)

	minVal = np.min(points[:,0])	
	maxVal = np.max(points[:,0])
	dCurrent = maxVal - minVal
	
	points = add_to_size_and_anticompress(points, emptySpace, compression=0.98) 

	areInside = pointsinside.pointsinside.pointsinpolygon(np.array(coord[:,1:],dtype="d"), np.array(points,dtype="d"), np.array(triangles))
	temp = np.column_stack((areInside, coord))

	finalPoints = [[y,a,b,c] for (x,y,a,b,c) in temp if(float(x)<0.5)]

	pid = {"Si" : 1, "Au" : 0, "O" : 2}

	with open("holedsilicaout.xyz","w") as f:
		f.write("%i\n" %(len(finalPoints)))
		f.write(header[1])
		k = 0
		for point in finalPoints:
			k += 1
			f.write("%2s %10.5f %10.5f %10.5f %i %i\n"  %(point[0].strip(), float(point[1]), float(point[2]), float(point[3]),pid[point[0].strip()], int(k)))
	


if(__name__ == "__main__"):	
	main()
