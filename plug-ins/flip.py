#!/usr/bin/python

import gimp
import array
import numpy as np

from gimpfu import *


def flip_main(image, drawable, flip = 0):


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

    np_array = np.array(src_pixels).reshape(bh,bw,bpp)
    np_array2 = np.zeros(bh * bw * bpp, dtype=int).reshape(bh,bw,bpp)

    if(flip == 0):
        for i in xrange(bh):
            np_array2[i,:,:] = np_array[-i-1,:,:]
    else:
        for i in xrange(bw):
            np_array2[:,i,:] = np_array[:,-i-1,:]

    np_array2 = np_array2.reshape(bh * bw * bpp)

    tmp_array= array.array('B', np_array2)
    src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
    drawable.flush()
    drawable.update(0, 0, image.width, image.height)
    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

register(
        "flip_plugin",
        "Flip",
        "Flip",
        "Josef Struz",
        "@JS",
        "2017",
        "Flip..",
        "RGB*, GRAY*",
        [
            (PF_IMAGE, "image", "takes current image", None),
            (PF_DRAWABLE, "drawable", "Input layer", None),
            (PF_OPTION, "filterer_by", "Flip: ", 0,
            (
                 ["Verticaly", "Horizontaly"]
            )
        )
        ],
        [],
        flip_main, menu="<Image>/Filters/JS-Filters" )

main()