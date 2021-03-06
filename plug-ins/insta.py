#!/usr/bin/python
import gimp
import array

from gimpfu import *

def get_in_range(number):
	if number > 255:
		number = 255
	if number < 0:
		number = 0
	return number


def insta_main(image, drawable):
	(bx1, by1, bx2, by2) = drawable.mask_bounds;

	pdb.gimp_image_undo_group_start(image)

	#dummy funkce (slouzi kvuli nastaveni undo)
	pdb.gimp_levels(drawable, HISTOGRAM_VALUE, 0, 255, 1.0, 0, 255)

	bw = bx2 - bx1
	bh = by2 - by1
	bpp = drawable.bpp

	#nacteni pixlu
	src_rgn = drawable.get_pixel_rgn(0, 0, image.width, image.height)
	src_pixels = array.array("B", src_rgn[bx1:bx2, by1:by2])

	for y in range(0, bh):
		for x in range(0, bw): 
			pos = (x + bw*y)*bpp
			c_array = src_pixels[pos:(pos+bpp)]
			inputRed = c_array[0]
			inputGreen = c_array[1]
			inputBlue = c_array[2]

			outputRed = (inputRed * .393) + (inputGreen *.769) + (inputBlue * .189)
			outputGreen = (inputRed * .349) + (inputGreen *.686) + (inputBlue * .168)
			outputBlue = (inputRed * .272) + (inputGreen *.534) + (inputBlue * .131)
			
			outputRed = get_in_range(outputRed)
			outputGreen = get_in_range(outputGreen)
			outputBlue = get_in_range(outputBlue)

			c_array[1] = int(outputRed)
			c_array[2] = int(outputBlue)
			c_array[0] = int(outputGreen)

			src_pixels[pos:(pos+bpp)] = c_array

	src_rgn[bx1:bx2, by1:by2] = src_pixels.tostring()
	drawable.flush()
	drawable.update(0, 0, image.width, image.height)
	gimp.displays_flush()

	pdb.gimp_image_undo_group_end(image)

register(
		"insta_plugin",
		"Insta",
		"Insta",
		"Josef Struz",
		"@JS",
		"2017",
		"Insta",
		"RGB*, GRAY*",
		[
			(PF_IMAGE, "image", "takes current image", None),
			(PF_DRAWABLE, "drawable", "Input layer", None),
		],
		[],
		insta_main, menu="<Image>/Filters/JS-Filters" )

main()