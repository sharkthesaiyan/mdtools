module goldfcc

contains

	function fcc_cube(n,l,four_n_cubic)
		integer, intent(in) :: n, four_n_cubic
		real(8), intent(in) :: l
		real(8) :: fcc_cube(four_n_cubic,3)
		integer :: i,j,a,b,c
		real(8) :: ax, ay, az	

		do i=0, n**3 - 1
			fcc_cube(4*i+1,:) = 0.0d0
			fcc_cube(4*i+2,:) = [0.0d0,0.5*l,0.5*l]			
			fcc_cube(4*i+3,:) = [0.5*l,0.0d0,0.5*l]
			fcc_cube(4*i+4,:) = [0.5*l,0.5*l,0.0d0]
		end do

		j = 0
		z: do c=0,n-1
			y: do b=0,n-1
				x: do a=0,n-1
					do k=0,3
						fcc_cube(4*j+k+1,:) = fcc_cube(4*j+k+1,:) + [a*l,b*l,c*l]
					end do
					j = j+1
				end do x
			end do y
		end do z

		!Centralize
		ax = sum(fcc_cube(:,1))/size(fcc_cube(:,1))
		ay = sum(fcc_cube(:,2))/size(fcc_cube(:,2))
		az = sum(fcc_cube(:,3))/size(fcc_cube(:,3))
		
		do i=1,four_n_cubic		
			fcc_cube(i,:) = fcc_cube(i,:) - [ax, ay, az]
		end do

	end function fcc_cube

end module goldfcc
