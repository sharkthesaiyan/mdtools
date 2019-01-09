#!/usr/bin/python

import matplotlib.pyplot as plt
import density
import xyzio
import numpy as np
import sys

def plotdensity(fname, refname):
	
	lattice, header = xyzio.readxyz(fname)
	lattice = np.asarray([[float(x[1]), float(x[2]), float(x[3])] for x in lattice])	

	reflattice, header = xyzio.readxyz(refname)
	reflattice = np.asarray([[float(x[1]), float(x[2]), float(x[3])] for x in reflattice])	

	
	densities = []
	step = 5.0
	maxi = 23
	r = 5.0
	for i in range(1,maxi):
		densities.append([1.0*density.density.cylinder_count(lattice, i*step, i*step+r)/(np.pi*((i*step+r)**2 - (i*step)**2)), (i*step + i*step+r)/2.0])

	densities = np.asarray(densities)


	#Reference densities (i.e. the first frame)
	
	refdensities = []
	for i in range(1,maxi):
		refdensities.append([1.0*density.density.cylinder_count(reflattice, i*step, i*step+r)/(np.pi*((i*step+r)**2 - (i*step)**2)), (i*step + i*step+r)/2.0])

	refdensities = np.asarray(refdensities)

	plt.plot(densities[:,1], densities[:,0]/refdensities[:,0])
	plt.show()

def main():
	fname = sys.argv[1]
	refname = sys.argv[2]
	plotdensity(fname, refname)

if __name__ == "__main__":
	main()
