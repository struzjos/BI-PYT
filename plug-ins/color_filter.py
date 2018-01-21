#!/usr/bin/python

import gimp
import array
import numpy as np
from numba import jit
import colorsys
import math
from gimpfu import *


def color_filter_main(image, drawable, color_org=(1.0,1.0,1.0), level=10, filterer_by=0):


    (bx1, by1, bx2, by2) = drawable.mask_bounds;

    pdb.gimp_image_undo_group_start(image)
    gimp.progress_update(0)

    #dummy funkce (vubec nic nedela, slouzi pro nastaveni undo)
    pdb.gimp_levels(drawable, HISTOGRAM_VALUE, 0, 255, 1.0, 0, 255)

    bw = bx2 - bx1
    bh = by2 - by1
    bpp = drawable.bpp

    #nacteni pixlu
    src_rgn = drawable.get_pixel_rgn(0, 0, image.width, image.height)
    src_pixels = array.array("B", src_rgn[bx1:bx2, by1:by2])
    np_array = np.array(src_pixels).reshape(bh*bw,bpp)

    @jit
    def apply_by_HSV(np_array, bh, bw, level, color_org):
        H, S, V = colorsys.rgb_to_hsv(color_org[0]/255.,color_org[1]/255.,color_org[2]/255.)
        H = int(H * 360)
        size = bh*bw
        for i in range(size):
            tmp_H, tmp_S, tmp_V = colorsys.rgb_to_hsv(np_array[i,0]/255.,np_array[i,1]/255.,np_array[i,2]/255.)
            tmp_H = int(tmp_H * 360)
            diff_H = min(abs(H - tmp_H), 360 - abs(H - tmp_H) )
            if( diff_H > level ):
                tmp_grey = np_array[i,0] * .299 + np_array[i,1] * .587 + np_array[i,2] * .114
                np_array[i,0] = tmp_grey
                np_array[i,1] = tmp_grey
                np_array[i,2] = tmp_grey

            gimp.progress_update(float(i)/size)

    @jit
    def apply_by_RGB(np_array, bh, bw, level, color_org):
        size = bh*bw
        for i in range(size):
            if(abs(np_array[i,0] - color_org[0]) > level or abs(np_array[i,1] - color_org[1]) > level or abs(np_array[i,2] - color_org[2]) > level ):
                tmp_grey = np_array[i,0] * .299 + np_array[i,1] * .587 + np_array[i,2] * .114
                np_array[i,0] = tmp_grey
                np_array[i,1] = tmp_grey
                np_array[i,2] = tmp_grey
            gimp.progress_update(float(i)/size)
    if(filterer_by):
        apply_by_RGB(np_array, bh, bw, level, color_org)
    else:
        apply_by_HSV(np_array, bh, bw, level, color_org)

    np_array = np_array.reshape(bw*bh*bpp,1)
    tmp_array = array.array('B', np_array)
    src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
    drawable.flush()
    drawable.update(0, 0, image.width, image.height)
    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

register(
    "color_filter_plugin",
    "Color_filter",
    "Color_filter",
    "Josef Struz",
    "@JS",
    "2017",
    "Color Filter..",
    "RGB*",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_COLOR,   "color",   "Color:", (1.0, 1.0, 1.0)),
        (PF_SLIDER, "level", "Range:", 10, (0,100,10)),
        (PF_OPTION, "filterer_by", "Filtered by: ", 0,
            (
                 ["HSV", "RGB"]
            )
        )
    ],
    [],
    color_filter_main, menu="<Image>/Filters/JS-Filters" )

main()