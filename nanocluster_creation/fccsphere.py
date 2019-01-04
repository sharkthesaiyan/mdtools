import numpy as np
import sys
import ntpath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#generates a .xyz file named fxxsphere.xyz with
#given details

def plot_cluster(coordinates):
	fig = plt.figure()
	ax = fig.add_subplot(111,projection="3d")

	coord = coordinates

	ax.scatter(coord[:,0].tolist(),coord[:,1].tolist(),coord[:,2].tolist())
	plt.grid()
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	ax.set_zlabel("z")
	plt.show()


def cutSphere(r, points):
	spherePoints = np.array([point for point in points if(np.linalg.norm(point)<=r)])	
	return(spherePoints)

def fcc_cube(n,l):
	coord = np.empty([4*n**3,3])	

	#Single cell:
	for i in range(0,n**3):
		coord[4*i,:]     = [0,0,0]
		coord[4*i + 1,:] = [0,0.5*l,0.5*l]
		coord[4*i + 2,:] = [0.5*l,0,0.5*l]		
		coord[4*i + 3,:] = [0.5*l,0.5*l,0]

	i = 0
	for x in range(0,n):
		for y in range(0,n):
			for z in range(0,n):
				coord[4*i:4*i+4] += [x*l,y*l,z*l]
				i += 1

	#Centralize
	ax = np.mean(coord[:,0])
	ay = np.mean(coord[:,1])
	az = np.mean(coord[:,2])

	coord -= [ax, ay, az]

	return(coord)


def main():
	if(len(sys.argv)>=4):	
		radius = float(sys.argv[1])
		n = int(sys.argv[2])
		compression = float(sys.argv[3])
		if(len(sys.argv) == 6):
			l = (1.0-compression)*float(sys.argv[4])
			element = sys.argv[5]
		else:
			l = (1.0-compression)*4.0782 #gold
			element = "Au"

		points = fcc_cube(n,l)

		finalPoints = cutSphere(radius*(1.0-compression), points)		
		
		plot_cluster(finalPoints)

		with open("fccsphere.xyz","w") as f:
			f.write("%i\n" %(len(finalPoints)))
			f.write("title row\n")
			k = 0
			for point in finalPoints:
				k += 1
				f.write("%s %10.5f %10.5f %10.5f 0 %i\n"  %(element, point[0], point[1], point[2], k))
	else:
		print("use: python3 %s radius n(cube unit cells to cut from) compression(0>c<=1)"%(ntpath.basename(sys.argv[0])))

main()
