def readxyz(fname):
	with open(fname,"r") as f:
		lines = f.readlines()

	header = lines[0:2]
	lattice = lines[2:]

	#Spilt, remove " " and "\n"
	lattice = [filter(lambda x: x!="\n", filter(None, a.split(" "))) for a in lattice]

	if(len(lattice[0])==9):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  float(a[6]), float(a[7]), float(a[8])] 
			  for a in lattice]
	elif(len(lattice[0])==6):
		lattice = [[a[0], float(a[1]), float(a[2]), float(a[3]), int(a[4]), int(a[5]),
			  0.0, 0.0, 0.0]
			  for a in lattice]

	return lattice, header

def splitxyz(fname):
	with open(fname,'r') as f:
		lines = f.readlines()

	nparticles = int(lines[0])

	frame = 1
	for i in range(len(lines)):
		if(i%(nparticles+2)==0):
			with open(fname+"_frame"+str(frame),'w') as f:
				for j in range(nparticles+2):
					f.write(lines[i+j])
			frame = frame + 1


