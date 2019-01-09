module density
	implicit none
	
contains

	subroutine cylinder_count(lattice, nlattice, minr, maxr, n)
		implicit none
		integer, intent(in) :: nlattice
		real(8), intent(in) :: lattice(nlattice,3), minr, maxr
		integer, intent(out) :: n
		real(8), parameter :: pi=3.14159265358979323
		integer :: i
		real(8) :: r

		n = 0

		do i=1,nlattice
			r = norm2(lattice(i,1:2))
			if( r > minr .and. r < maxr ) then
				n = n+1
			end if
		end do

	end subroutine cylinder_count

end module density
