import random
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D
import pointsinside

#Moller-Trumbore intersection from wikipedia
def triangle_intersect(p0, p, triangle):
	epsilon = 0.000001
	vertex0 = triangle[0,:]
	vertex1 = triangle[1,:]
	vertex2 = triangle[2,:]
	edge1 = vertex1 - vertex0
	edge2 = vertex2 - vertex0

	h = np.cross(p,edge2)
	a = np.dot(edge1,h)

	if(a > -1.0*epsilon and a < epsilon ):
		return False

	f = 1.0/a
	s = p0 - vertex0
	u = f*np.dot(s,h)

	if(u < 0.0 or  u > 1.0):
		return False

	q = np.cross(s,edge1)
	v = f*np.dot(p,q)
	
	if(v < 0.0 or u+v>1.0):
		return False

	t = f*np.dot(edge2,q)
	if(t>epsilon):
		intersectPoint = p0 + p*t
		return True
	else:
		return False

def read_vtk(fname):
	with open(fname) as f:
		lines = f.readlines()

	if(lines[4][0:6] == "POINTS"):
		#Get the number of points from the 5th row
		n = int(lines[4].split(" ")[1])

		#Read the points using the number of points
		points = [line.strip().split(" ")[0:3] for line in lines[5:4+n+1]]	

	#Convert to float
	points = [[float(x), float(y), float(z)] for [x,y,z] in points]

	#Now load the triangles
	cellLine = [[line, i] for i, line in enumerate(lines) if line.find("CELLS")>=0][0]
	lineNumber = cellLine[1]
	triangleCount = int(cellLine[0].strip().split(" ")[1])
	#Text rows to integer arrays
	triangles = lines[lineNumber+1:lineNumber+1+triangleCount]
	triangles = [line.strip() for line in triangles]
	triangles = [line.split(" ")[1:4] for line in triangles]
	triangles = [[int(a), int(b), int(c)] for [a,b,c] in triangles]	

	#Both points and triangles to numpy array as they are more confortable to work with
	triangles = np.array(triangles)
	points = np.array(points)

	return points, triangles


def isInsidePolygon(p0, points, triangles):
	intersectCount = 0
	p = np.array([500,500,500]) #Set here point that is outside the polygon
	for triangle in triangles:
		absTriangle = np.array([points[triangle[0]], points[triangle[1]], points[triangle[2]]])
		#If you change p look carefully the next few lines might not work
		#because this depends on the direction vector from p0 to p
		if(sum([vertice[0] < p0[0] or vertice[1] < p0[1] or vertice[2] < p0[2] for vertice in absTriangle])==3):
			continue

		intersect = triangle_intersect(p0, p, absTriangle)
		if(intersect == True):		
			intersectCount += 1
		
	if(intersectCount%2 == 1):
		#Is inside
		return True
	else:
		#Is outside
		return False

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

def scale_to(points, newRadius, direction=0):
	minVal = np.min(points[:,direction])	
	maxVal = np.max(points[:,direction])
	radius = maxVal - minVal
	c = newRadius/radius
	print "radius=%f, c=%f" %(radius, c)

	points = points*c

	return points

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

	return coord

def write_vtk(fname, points, triangles):
	with open(fname, "w") as f:
		f.write("# vtk DataFile Version 3.0\n")
		f.write("# Triangle mesh\n")
		f.write("ASCII\n")
		f.write("DATASET UNSTRUCTURED_GRID\n")
		f.write("POINTS %i double\n" %(len(points)))
		for point in points:
			f.write("%f %f %f\n" %(point[0],point[1],point[2]))

		f.write("\n")
		f.write("CELLS %i %i\n" %(len(triangles), len(triangles)*4))
		for triangle in triangles:
			f.write("3 %i %i %i\n" %(triangle[0], triangle[1], triangle[2]))
		f.write("\n")
		f.write("CELL_TYPES %i\n" %(len(triangles)))
		for triangle in triangles:
			f.write("5\n")


def main():
	#coord = points cut from fcc
	#points = points that define the shape when triangulized
	#finalPoints = points that define the final nanoparticle (also contains interior points)

	n = int(sys.argv[1])
	meshfile = sys.argv[2]
	atomCountOrig = int(sys.argv[3])
	iterations = int(sys.argv[4])
	if(len(sys.argv)==6):
		atomCount = int(sys.argv[5])

	coord = fcc_cube(n, 4.0782)
	points, triangles = read_vtk(meshfile)

	for j in range(iterations):
		if(j>0 or len(sys.argv)==6):
			#Scaling guess parameters
			xmax = np.max([x for [x,y,z] in points])
			xmin = np.min([x for [x,y,z] in points])
			currentD = xmax - xmin
			#scale the boundary points according to ratio of atom count compared to target count
			points = scale_to(points, currentD*(1.0*atomCountOrig/atomCount*1.0)**(1.0/3.0), direction=0)
			if(atomCountOrig < atomCount and j>0):
				coord = finalPoints
			else:
				coord = fcc_cube(n, 4.0782)

		finalPoints = []
		
		i = 0
		ncoord = len(coord)
		percent = ncoord/100

		#Trivial conditions to see if point is inside
		#Sphere that cointains all border points
		outsideR = np.max([np.sqrt(x**2 + y**2 + z**2) for [x,y,z] in points])
		#Sphere that's completely inside the shape
		insideR = np.min([np.sqrt(x**2 + y**2 + z**2) for [x,y,z] in points])

		

		areInside = pointsinside.pointsinside.pointsinpolygon(np.array(coord,dtype="d"), np.array(points,dtype="d"), np.array(triangles))

		temp = np.column_stack((areInside, coord))

		finalPoints = np.array([[a,b,c] for (x,a,b,c) in temp if(x>0.5)])
		atomCount = len(finalPoints)
		print "round %i done" %(j)
		print "atom count=%i" %(atomCount)


	print atomCount
	plot_cluster(finalPoints)

	#Compress 2%
	finalPoints = finalPoints*0.98

	with open("out.xyz","w") as f:
		f.write("%i\n" %(len(finalPoints)))
		f.write("title row, I have no clue\n")
		k = 0
		for point in finalPoints:
			k += 1
			f.write("Au %10.5f %10.5f %10.5f 0 %i\n"  %(point[0], point[1], point[2], k))

	#Write out the current .vtk for further use
	write_vtk("out_surface.vtk", points, triangles)

main()
