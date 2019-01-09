import numpy as np
import density as den
import sys
import xyzio

def numberDensityAvoidGold(fname):
	lattice, header = xyzio.readxyz(fname)
	gold = np.asarray([[a[1],a[2],a[3]] for a in lattice if a[0].find("Au")>=0])
	z = [a[2] for a in gold]
	zmin = np.min(z)-1.0
	zmax = np.max(z)+1.0

	newLattice = np.asarray([[a[1],a[2],a[3]] for a in lattice if a[3]>zmax or a[3]<zmin])

	newZmin = np.min(newLattice[:,2])
	newZmax = np.max(newLattice[:,2])
	
	h = np.abs(zmin-newZmin) + np.abs(zmax-newZmax)

	nlattice = len(newLattice[:,0])
	r = 5.0

	#print den.density.cylinder_count.__doc__

	for i in range(0,22):
		minr = i*r
		maxr = (i+1)*r
		n = den.density.cylinder_count(newLattice, minr, maxr)/(h*np.pi*(maxr**2 - minr**2))
		print np.mean([minr,maxr]), n
		#print n,
	#print ""

def main():
	numberDensityAvoidGold(sys.argv[1])

main()
