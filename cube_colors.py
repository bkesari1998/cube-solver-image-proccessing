from PIL import Image
import sys

def open_image(file_path):
	'''
	Opens an image file for processing
	Precondition: file_path is a valid path to an image file
	Postcondition: returns an object containing the image converted to rgb values
	'''
	
	img = Image.open(file_path)
	img_rgb = img.convert("RGB")
	img.close()

	return img_rgb

def get_sq_width_height(side_rgb):
	'''
	Gets square width, and square height of an Rubik's Cube side image
	Precondition: side_rgb is a valid image object converted to rgb values
	Postcondition: returns the square width, and square height of the Rubik's Cube image
	'''

	num_sq_in_row = 3

	width, height = side_rgb.size
	sq_width = width / num_sq_in_row
	sq_height = height / num_sq_in_row

	return sq_width, sq_height

def get_sq_rgb(side_rgb, x_coord, y_coord, sq_width, sq_height):
	'''
	Determines the rgb value of a square on the side of a Rubik's Cube
	Precondition: side_rgb is a valid image object converted to rgb values.
	x_coord is the x_coordinate location near the left edge of the square.
	y_coord is the y_coordinate location near the top edge of the square.
	sq_width is the width in pixels of 1 square on the rubiks cube.
	sq_height is the height in pixels of 1 square on the rubiks cube.
	Postcondition: returns the average rgb value  of the square
	'''

	r_sum = 0
	g_sum = 0
	b_sum = 0

	# Get the average rgb value of 16  locations on the square
	for pixel in range(4):
		for pixel in range(4):
			(r, g, b) = side_rgb.getpixel((x_coord, y_coord))
			r_sum = r_sum + r
			g_sum = g_sum + g
			b_sum = b_sum + b
			x_coord = x_coord + sq_width / 5
		
		x_coord = x_coord - (4 / 5) *  sq_width 
		y_coord = y_coord + sq_height / 5

	r_avg = r_sum / 16
	g_avg = g_sum / 16
	b_avg = b_sum / 16

	return round(r_avg), round(g_avg), round(b_avg)

def get_sq_color(r, g, b):
	'''
	Determines the color of a square on the side of a Rubik's Cube.
	This function uses predefined rgb values corresponding to the specific Rubik's cube in use.
	Preconditon: r, g, and b are valid integers corresponding to the rgb value of a square on a Rubik's cube
	Postconditon: returns a char corresponding to the color of the square
	'''

	# Initialize lists that hold a color's rgb value and abbrieviation
	yellow = [(211, 206, 54), 'y']
	white = [(204, 192, 173), 'w']
	red = [(170, 47, 26), 'r']
	orange = [(217, 102, 27), 'o']
	blue = [(62, 112, 163), 'b']
	green = [(106, 190, 95), 'g']

	# Initialize list that holds the colors
	colors = [yellow, white, red, orange, blue, green]

	# Compare rgb value of square with rgb value of each color

	# Create a list to hold the minimum difference between the square's rgb value and the abbrieviation of that color
	# Initialized to hold an arbitrary difference and 'u' to represent undefined
	col_match = [1000, 'u']
	for color in colors:
		(col_r, col_g, col_b) = color[0]
		diff = get_rgb_diff(r, g, b, col_r, col_g, col_b)
		# Check if diff is less than value in col_match
		if (diff < col_match[0]):
			# Redefine col_match
			col_match = [diff, color[1]]
	# Return the abbreiviation of the matching color
	return col_match[1]

def get_rgb_diff(pix_r, pix_g, pix_b, col_r, col_g, col_b):
	'''
	Calculates the sum of the difference between a pixel's rgb values and a predefined color's rgb values
	Precondition: pix_r, pix_g and pix_b are integers corresponding to the rgb values of a pixel of an image
	col_r, col_g, and col_b are integers corresponding to the rgb values of a predetermined color
	Postcondition: returns the sum of the differences between the pixel's rgb values and the predefined color's rgb values
	'''
	
	# Calculate magnitude of differences
	r_diff = abs(pix_r - col_r)
	g_diff = abs(pix_g - col_g)
	b_diff = abs(pix_b - col_b)

	# Return sum of differences
	return r_diff + g_diff + b_diff

def get_color_rgb(solved_path):
	'''
	Ouputs the average rgb value representing the color on one solved side of a square. Used to tune other functions.
	Precondition: solved_path is a path to an image of a solved side of a Rubik's cube.
	Postcondition: Returns the average rgb value of the side
	'''
	
	num_squares_on_face = 9
	num_rows_on_side = 3
	num_squares_in_row = 3

	r_sum = 0
	g_sum = 0
	b_sum = 0

	# Convert image to rgb
	solved_rgb = open_image(solved_path)
	width, height = solved_rgb.size

	# Get image size data
	sq_width, sq_height = get_sq_width_height(solved_rgb)

	# Loop for each square on side
	x_coord = sq_width / 5
	y_coord = sq_height / 5

	for row in range(num_rows_on_side):
		for square in range(num_squares_in_row): 
			# Get average rgb value of the square
			r_avg_sq, g_avg_sq, b_avg_sq = get_sq_rgb(solved_rgb, x_coord, y_coord, sq_width, sq_height)
			
			# Update sums
			r_sum = r_sum + r_avg_sq
			g_sum = g_sum + g_avg_sq
			b_sum = b_sum + b_avg_sq
	
			# Advance to next square
			x_coord = x_coord + sq_width

		# Reset x_coord to left edge of square and advance y_coord to next row
		x_coord = sq_width / 5
		y_coord = y_coord + sq_height
	
	# Calculate averages for the side
	r_avg = r_sum / num_squares_on_face
	g_avg = g_sum / num_squares_on_face
	b_avg = b_sum / num_squares_on_face

	return round(r_avg), round(g_avg), round(b_avg)	

def output_cube_colors(side_1_path, side_2_path, side_3_path, side_4_path, side_5_path, side_6_path):
	'''
	Outputs a string of color abbrieviations corresponding to a Rubik's Cube permutation
	Precondition: parameters are each a path to an image of 1 side of a Rubik's Cube
	Postcondition: prints a string of color abbrieviations to the terminal
	'''
	
	num_squares_in_row = 3
	num_rows_on_side = 3

	color_string = []

	# Store the image paths in a list
	side_paths = [side_1_path, side_2_path, side_3_path, side_4_path, side_5_path, side_6_path]
	
	# Loop through each image
	for side_img in side_paths:
		# Convert image to rgb
		side_rgb = open_image(side_img)

		# Get image size data
		sq_width, sq_height = get_sq_width_height(side_rgb)

		# Loop for each square on side
		x_coord = sq_width / 5
		y_coord = sq_width / 5
		
		for row in range(num_rows_on_side):
			for square in range(num_squares_in_row):
				
				# Get average rgb value of square
				r_avg, g_avg, b_avg = get_sq_rgb(side_rgb, x_coord, y_coord, sq_width, sq_height)
				
				# Get color abbrieviation of the square
				col_abbrieve = get_sq_color(r_avg, g_avg, b_avg)

				# Append abbrieviation to color_string
				color_string.append(col_abbrieve)

				# Advance x_coord to next square in row
				x_coord = x_coord + sq_width
			
			# Reset x_coord to left edge of sqare and advance y_coord to next row
			x_coord = sq_width / 5
			y_coord = y_coord + sq_height
		
	# Print the string
	for i in range(len(color_string)):
		sys.stdout.write(color_string[i])

	sys.stdout.write('\n')
