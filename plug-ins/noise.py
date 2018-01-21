#!/usr/bin/python

import gimp
import array
import numpy as np

from gimpfu import *

def noise_main(image, drawable, level=10, separate=True):

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
     
    out = np.zeros([bh,bw,bpp], dtype=int)

    if separate:
        for canal in range(bpp):
            tmp_noise_array = np.random.uniform(-level,level,(bh,bw))
            out[:,:,canal] = np_array[:,:,canal] + tmp_noise_array
    else:
        tmp_noise_array = np.random.uniform(-level,level,(bh,bw,1))
        out = np_array + tmp_noise_array

    out = np.minimum(np.maximum(out, 0), 255)

    out = out.reshape(bw*bh*bpp,1)
    tmp_array = array.array('B', out)
    src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
    drawable.flush()
    drawable.update(0, 0, image.width, image.height)
    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

register(
    "noise_plugin",
    "Noise",
    "Noise",
    "Josef Struz",
    "@JS",
    "2017",
    "Noise..",
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_SLIDER, "level", "noise level:", 10, (0,255,10)),
        (PF_BOOL, "separate_colors", "Separate colors:", True),
    ],
    [],
    noise_main, menu="<Image>/Filters/JS-Filters" )

main()