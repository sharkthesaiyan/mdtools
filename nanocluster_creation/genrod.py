#!/usr/bin/python
import numpy as np
import sys
import goldfcc

def cutSphere(block, r):
	print np.min(block[:,1]), np.max(block[:,1]), np.max(block[:,1]) - np.min(block[:,1])
	return [a for a in block if(np.linalg.norm(a) < r)]

def cutCylinder(block,r,z):
	return [ a for a in block if(np.linalg.norm(a[0::2]) < r and np.absolute(a[1]) < z*0.5 )]

def generateRod(z,r,n):
	#goldBlock = goldfcc.goldfcc.fcc_cube(n, 4.0782,4*n**3)	
	goldBlock = goldfcc.goldfcc.fcc_cube(n, 4.0782)

	cylinder = cutCylinder(goldBlock, r, z)

	#Take cylinder heads
	head1 = np.asarray([ a for a in cylinder if( a[1] > z*0.5-r)])
	head2 = np.asarray([ a for a in cylinder if( a[1] < -z*0.5+r)])
	print len(head1), len(head2), len(cylinder)
	#Round heads
	head1 = [0.0,0.5*z-r,0.0] + np.asarray(cutSphere(np.asarray(head1) - [0.0,0.5*z-r,0.0],r))
	head2 = [0.0,-0.5*z+r,0.0] + np.asarray(cutSphere(np.asarray(head2) - [0.0,-0.5*z+r,0.0], r))

	#Cut ends
	print len(head1), len(head2), len(cylinder)

	cylinder = [ a for a in cylinder if(np.absolute(a[1])<z*0.5-r)]
	
	#Add spherical ends
	cylinder = head1.tolist()+head2.tolist()+cylinder
	with open("goldrod.xyz","w") as f:
		f.write(str(len(cylinder))+"\n")
		f.write("a b c d e boxsize 200.0 200.0 200.0\n")
		k = 0
		for a in cylinder:
			f.write("Au %10.5f %10.5f %10.5f 0 %i 0.0 0.0 0.0\n" %(a[0], a[1], a[2], k))
			k = k+1

def main():
	z = float(sys.argv[1])
	r = float(sys.argv[2])
	if(len(sys.argv)==4):	
		n = int(sys.argv[3])
	else:
		n = 50
	generateRod(z,r,n)


if __name__ == "__main__":
	main()
