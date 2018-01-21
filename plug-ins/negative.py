#!/usr/bin/python

from subprocess import call
import gimp
import array
import numpy as np

from gimpfu import *


def negative_main(image, drawable):


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

	np_array = (np.array(src_pixels) - 255) * -1

	tmp_array= array.array('B', np_array)
	src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
	drawable.flush()
	drawable.update(0, 0, image.width, image.height)
	gimp.displays_flush()

	pdb.gimp_image_undo_group_end(image)

register(
		"negative_plugin",
		"Negative",
		"Negative",
		"Josef Struz",
		"@JS",
		"2017",
		"Negative",
		"RGB*, GRAY*",
		[
			(PF_IMAGE, "image", "takes current image", None),
			(PF_DRAWABLE, "drawable", "Input layer", None),
		],
		[],
		negative_main, menu="<Image>/Filters/JS-Filters" )

main()