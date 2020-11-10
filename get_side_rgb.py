from cube_colors import *

solved_sides = ["./solved_img/blue.jpg", "./solved_img/green.jpg", "./solved_img/orange.jpg", "./solved_img/red.jpg", "./solved_img/white.jpg", "./solved_img/yellow.jpg"]

# Loop for each side on cube
for side in solved_sides:
	# Get average rgb value of side
	r, g, b = get_color_rgb(side)
	
	# Print rgb value
	print("(" + str(r) + ", " + str(g) + ", " + str(b) + ")")
