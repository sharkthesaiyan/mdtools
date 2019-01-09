module pointsinside
	implicit none

contains

	function cross(a, b)
	  real(kind=8), dimension(3) :: cross
	  real(kind=8), dimension(3), intent(in) :: a, b

	  cross(1) = (a(2) * b(3)) - (a(3) * b(2))
	  cross(2) = (a(3) * b(1)) - (a(1) * b(3))
	  cross(3) = (a(1) * b(2)) - (a(2) * b(1))

	end function cross

	integer function triangle_intersect(p0, p, triangle)
		implicit none
		real(kind=8), intent(in) :: p(3), p0(3), triangle(3,3)
		real(kind=8) :: vertex0(3), vertex1(3), vertex2(3), edge1(3), edge2(3), h(3), a, f, s(3), u, q(3), v, t, eps

		eps = 0.00000001d0
		vertex0 = triangle(1,:)
		vertex1 = triangle(2,:)
		vertex2 = triangle(3,:)
		edge1 = vertex1 - vertex0
		edge2 = vertex2 - vertex0

		h = cross(p,edge2)
		a = dot_product(edge1,h)

		if(a > -1.0*eps .and. a < eps) then
			triangle_intersect = 0
			return
		end if

		f = 1.0/a
		s = p0 - vertex0
		u = f*dot_product(s,h)

		if(u < 0.0 .or.  u > 1.0) then
			triangle_intersect = 0
			return
		end if

		q = cross(s,edge1)
		v = f*dot_product(p,q)

		if(v < 0.0 .or. u+v>1.0) then
			triangle_intersect = 0
			return
		end if

		t = f*dot_product(edge2,q)
		if(t>eps) then
			triangle_intersect = 1
			return
		else
			triangle_intersect = 0
			return
		end if

		triangle_intersect = -1
		return
	end function triangle_intersect

	integer function insidepolygon(p0, points, np, triangles, nt)
		implicit none
		integer, intent(in) :: nt, np
		integer, intent(in) :: triangles(nt,3)
		real(kind=8), intent(in) :: points(np,3), p0(3)

		integer :: intersections, i, intersect
		real(kind=8) :: absTriangle(3,3), p(3)=[500.0d0,500.0d0,500.0d0]

		intersections = 0
		do i=1, nt
			absTriangle(1,:) = points(triangles(i,1)+1,:)
			absTriangle(2,:) = points(triangles(i,2)+1,:)	
			absTriangle(3,:) = points(triangles(i,3)+1,:)


			if( count(absTriangle(:,1) < p0(1)) == 3 .or. &
			&   count(absTriangle(:,2) < p0(2)) == 3 .or. count(absTriangle(:,3) < p0(3)) == 3 ) then
				cycle
			end if

			intersect = triangle_intersect(p0, p, absTriangle)

			if(intersect==1) then
				intersections = intersections + 1
			end if
		end do

		if(mod(intersections,2)==1) then
			insidepolygon = 1
		else
			insidepolygon = 0
		end if

	end function insidepolygon

	subroutine pointsinpolygon(coordinates,nc,points,np,triangles,nt,outvalues)
		implicit none
		integer, intent(in) :: nt, np, nc
		integer, intent(in) :: triangles(nt,3)
		real(kind=8), intent(in) :: points(np,3), coordinates(nc,3)
		integer, intent(out) :: outvalues(nc)
		integer :: i,j, value
		real(kind=8) :: p(3)
		
		outvalues = 0

		do i=1,nc
			p = coordinates(i,:)
			value = insidepolygon(p, points, np, triangles, nt)
			if(value==1) then
				outvalues(i) = 1
			else
				outvalues(i) = 0
			end if
		end do
		
	end subroutine pointsinpolygon

end module pointsinside

