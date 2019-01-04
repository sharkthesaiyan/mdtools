import numpy as np
import sys

def readxyz(fname):
	with open(fname,"r") as f:
		lines = f.readlines()

	header = lines[0:2]
	lattice = lines[2:]

	lattice = [filter(None, a.split(" ")) for a in lattice]

	lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
		  float(a[6]), float(a[7]), float(a[8])] 
		  for a in lattice]

	return lattice, header
	

def writexyz(fname, lattice, header):
	with open(fname,"w") as f:
		f.write("%i\n" %(len(lattice)))
		f.write(header[1])
		for atom in lattice:
			f.write("%s %f %f %f %i %i %f %f %f\n" %(atom[0], atom[1],atom[2],
				atom[3],atom[4],atom[5],atom[6],atom[7],atom[8]))


def digasphericalhole(radius, lattice):

	holesomelattice = []
	for atom in lattice:
		r = np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2)	
		if(r >= radius):
			holesomelattice.append(atom)

	return holesomelattice

def main():
	radius = float(sys.argv[2])
	xyzfile = sys.argv[1]


	lattice, header = readxyz(xyzfile)
	lattice = digasphericalhole(radius, lattice)

	writexyz("holesomelattice.xyz", lattice, header)

main()
