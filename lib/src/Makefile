all: goldfcc.so pointsinside.so

goldfcc.so: goldfcc.f95
	f2py -c goldfcc.f95 -m goldfcc
pointsinside.so: pointsinside.f95
	f2py -c pointsinside.f95 -m pointsinside
