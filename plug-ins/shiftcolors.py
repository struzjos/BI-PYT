#!/usr/bin/python

from subprocess import call
import gimp
import array
import numpy as np

from gimpfu import *


def shift_colors_main(image, drawable, level):


	(bx1, by1, bx2, by2) = drawable.mask_bounds;


	pdb.gimp_image_undo_group_start(image)

	#dummy funkce (vubec nic nedela, slouzi pro nastaveni undo)
	pdb.gimp_levels(drawable, HISTOGRAM_VALUE, 0, 255, 1.0, 0, 255)

	bw = bx2 - bx1
	bh = by2 - by1
	bpp = drawable.bpp

	#nacteni pixlu
	src_rgn = drawable.get_pixel_rgn(0, 0, image.width, image.height)
	src_pixels = array.array("B", src_rgn[bx1:bx2, by1:by2])

	np_array = np.array(src_pixels) + int(level)

	np_array = np.minimum(np.maximum(np_array, 0), 255)

	tmp_array= array.array('B', np_array)
	src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
	drawable.flush()
	drawable.update(0, 0, image.width, image.height)
	gimp.displays_flush()

	pdb.gimp_image_undo_group_end(image)

register(
		"Shift_colors_plugin",
		"Shift_colors",
		"Shift_colors",
		"Josef Struz",
		"@JS",
		"2017",
		"Shift colors..",
		"RGB*, GRAY*",
		[
			(PF_IMAGE, "image", "takes current image", None),
			(PF_DRAWABLE, "drawable", "Input layer", None),
	        (PF_SLIDER, "level", "Level:", 0, (-255,255,0)),
		],
		[],
		shift_colors_main, menu="<Image>/Filters/JS-Filters" )

main()