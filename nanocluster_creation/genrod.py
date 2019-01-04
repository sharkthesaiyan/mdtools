#!/usr/bin/python
import numpy as np
import sys
import goldfcc 
import ntpath
#don't get confused by the name, other elements can be used
#gold used to be the only one

def cutSphere(block, r):
	return([a for a in block if(np.linalg.norm(a) < r)])

def cutCylinder(block,r,z):
	return([ a for a in block if(np.linalg.norm(a[0::2]) < r and np.absolute(a[1]) < z*0.5 )])

def generateRod(z,r,n,l,element):
	fccBlock = goldfcc.goldfcc.fcc_cube(n, l,4*n**3)

	cylinder = cutCylinder(fccBlock, r, z)

	#Take cylinder heads
	head1 = np.asarray([ a for a in cylinder if( a[1] > z*0.5-r)])
	head2 = np.asarray([ a for a in cylinder if( a[1] < -z*0.5+r)])
	#Round heads
	head1 = [0.0,0.5*z-r,0.0] + np.asarray(cutSphere(np.asarray(head1) - [0.0,0.5*z-r,0.0],r))
	head2 = [0.0,-0.5*z+r,0.0] + np.asarray(cutSphere(np.asarray(head2) - [0.0,-0.5*z+r,0.0], r))

	#Cut ends
	cylinder = [ a for a in cylinder if(np.absolute(a[1])<z*0.5-r)]
	
	#Add spherical ends
	cylinder = head1.tolist()+head2.tolist()+cylinder
	with open("fccrod.xyz","w") as f:
		f.write(str(len(cylinder))+"\n")
		f.write("a b c d e boxsize 200.0 200.0 200.0\n")
		k = 0
		for a in cylinder:
			f.write("%s %10.5f %10.5f %10.5f 0 %i 0.0 0.0 0.0\n" %(element, a[0], a[1], a[2], k))
			k = k+1

def main():
	if(len(sys.argv)>=3):
		z = float(sys.argv[1])
		r = float(sys.argv[2])
		if(len(sys.argv)>=4):	
			n = int(sys.argv[3])
		else:
			n = 50
		if(len(sys.argv)==5):
			l = float(sys.argv[4])
		else:
			l = 4.0782 #Au

		if(len(sys.argv)==6):
			element = sys.argv[5]
		else:
			element = "Au"

		generateRod(z,r,n,l,element)
	else:
		print "use: python %s zlen r"%(ntpath.basename(sys.argv[0]))

if __name__ == "__main__":
	main()
