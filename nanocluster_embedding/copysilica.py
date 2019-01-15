import numpy as np
import sys
import os

def readxyz(fname):
	with open(fname,"r") as f:
		lines = f.readlines()

	header = lines[0:2]
	lattice = lines[2:]

	lattice = [filter(None, a.split(" ")) for a in lattice]

	if(len(lattice[0])==10):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  float(a[6]), float(a[7]), float(a[8])] 
			  for a in lattice]

	elif(len(lattice[0])==7):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  0.0, 0.0, 0.0] 
			  for a in lattice]

	return lattice, header

def writexyz(fname, lattice, header):
	with open(fname,"w") as f:
		f.write(header[0])
		f.write(header[1])
		i = 1
		for atom in lattice:
			f.write("%s %f %f %f %i %i %f %f %f\n" %(atom[0], atom[1],atom[2],
				atom[3],atom[4],i,atom[6],atom[7],atom[8]))
			i += 1

def copylattice(lattice, header, nx, ny, nz):
	xlen = float(header[1].split(" ")[6])
	ylen = float(header[1].split(" ")[7])
	zlen = float(header[1].split(" ")[8])

	finalLattice = []

	for i in range(0,nx):
		for j in range(0,ny):
			for k in range(0,nz):
				latticeCopy = [[a[0],a[1]+i*xlen, a[2]+j*ylen, a[3]+k*zlen,
						a[4],a[5],a[6],a[7],a[8]] for a in lattice]
				finalLattice = finalLattice + latticeCopy



	newHeader = []
	newHeader.append(str(len(finalLattice))+"\n")
	newHeader.append("a b c d e boxsize %7.3f %7.3f %7.3f\n" %(xlen*nx, ylen*ny, zlen*nz))

	return finalLattice, newHeader


def main():

	fname = os.path.dirname(sys.argv[0])+"/SilicaL_4x1.xyz"
	nx = int(sys.argv[1])
	ny = int(sys.argv[2])
	nz = int(sys.argv[3])

	lattice, header = readxyz(fname)

	print lattice[0]

	lattice, header = copylattice(lattice, header, nx, ny, nz)
	writexyz("silicacopy_out.xyz", lattice, header)

main()
