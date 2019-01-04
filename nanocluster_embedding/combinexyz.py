import sys
import numpy as np

def readxyz(fname):
	with open(fname,"r") as f:
		lines = f.readlines()

	header = lines[0:2]
	lattice = lines[2:]

	lattice = [filter(None, a.split(" ")) for a in lattice]

	if(len(lattice[0])==9):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  float(a[6]), float(a[7]), float(a[8])] 
			  for a in lattice]
	elif(len(lattice[0])==6):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  0.0, 0.0, 0.0] 
			  for a in lattice]

	return lattice, header

def combinewritexyz(fname, lattice1, lattice2, header):
	with open(fname,"w") as f:
		f.write("%i\n" %(len(lattice1+lattice2)))
		f.write(header[1])
		i = 1
		for atom in lattice1 + lattice2:
			f.write("%s %f %f %f %i %i %f %f %f \n" %(atom[0], atom[1],atom[2],
				atom[3],atom[4],i,atom[6],atom[7],atom[8]))
			i = i+1

def main():
	inputFile1 = sys.argv[1]
	inputFile2 = sys.argv[2]
	
	lattice1, header1 = readxyz(inputFile1)
	lattice2, header2 = readxyz(inputFile2)

	combinewritexyz("combined.xyz", lattice1, lattice2, header1)

main()
