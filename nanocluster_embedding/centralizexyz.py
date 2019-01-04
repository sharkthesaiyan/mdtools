import numpy as np
import sys

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

def writexyz(fname, lattice,header):
	with open(fname,"w") as f:
		f.write(header[0])
		f.write(header[1])
		for atom in lattice:
			f.write("%s %f %f %f %i %i %f %f %f\n" %(atom[0], atom[1],atom[2],
				atom[3],atom[4],atom[5],atom[6],atom[7],atom[8]))

def centralize(lattice):

	xmean = np.mean([float(a[1]) for a in lattice])	
	ymean = np.mean([float(a[2]) for a in lattice])
	zmean = np.mean([float(a[3]) for a in lattice])

	lattice = [[a[0], a[1]-xmean, a[2]-ymean, a[3]-zmean,a[4],a[5],a[6],a[7],a[8]] for a in lattice]

	xmean = np.mean([float(a[1]) for a in lattice])	
	ymean = np.mean([float(a[2]) for a in lattice])
	zmean = np.mean([float(a[3]) for a in lattice])

	print [xmean, ymean, zmean]

	return lattice

def main():
	fileName = sys.argv[1]
	lattice, header = readxyz(fileName)

	print lattice[0]

	lattice = centralize(lattice)

	writexyz(fileName.split(".")[0]+"_centralized.xyz", lattice, header)

main()
