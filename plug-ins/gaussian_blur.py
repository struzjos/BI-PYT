#!/usr/bin/python

import gimp
import array
import numpy as np
from numba import jit

from gimpfu import *


def gaussian_blur_main(image, drawable):

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
     
    # definice filteru
    filter = np.array([
        [1./16, 2./16, 1./16],
        [2./16, 4./16, 2./16],
        [1./16, 2./16, 1./16],
    ])
    
    # aplikace filteru
    @jit(nopython=True, cache=True)
    def apply_filter_body(data, mask, output):
        
        data_w, data_h = data.shape

        for y in range(1, data_h - 1):
            for x in range(1, data_w - 1):
                cut = data[x-1:x+2,y-1:y+2]
                output[x, y] = (cut * mask).sum()

    def apply_filter(data, mask, output):

        data_w, data_h = data.shape

        cut = np.array([data[0,0],data[0,0],data[0,1],data[0,0],data[0,0],data[0,1],data[1,0],data[1,0],data[1,1]]).reshape(3,3)
        output[0, 0] = (cut * mask).sum()

        cut = np.array([data[0,data_h-2],data[0,data_h-1],data[0,data_h-1],data[0,data_h-2],data[0,data_h-1],data[0,data_h-1],data[1,data_h-2],data[1,data_h-1],data[1,data_h-1]]).reshape(3,3)
        output[0, data_h - 1] = (cut * mask).sum()

        cut = np.array([data[data_w-2,0],data[data_w-2,0],data[data_w-2,1],data[data_w-1,0],data[data_w-1,0],data[data_w-1,1],data[data_w-1,0],data[data_w-1,0],data[data_w-1,1]]).reshape(3,3)
        output[data_w-1, 0] = (cut * mask).sum()

        cut = np.array([data[data_w-2,data_h-2],data[data_w-2,data_h-1],data[data_w-2,data_h-1],data[data_w-1,data_h-2],data[data_w-1,data_h-1],data[data_w-1,data_h-1],data[data_w-1,data_h-2],data[data_w-1,data_h-1],data[data_w-1,data_h-1]]).reshape(3,3)
        output[data_w-1, data_h-1] = (cut * mask).sum()

        for y in range(1, data_h - 1):
            cut = data[[0,0,1],y-1:y+2]
            output[0, y] = (cut * mask).sum()
            cut = data[[data_w-2,data_w-1,data_w-1], y-1:y+2]
            output[data_w-1, y] = (cut * mask).sum()

        for x in range(1, data_w - 1):
            cut = data[x-1:x+2, [0,0,1]]
            output[x,0] = (cut * mask).sum()
            cut = data[x-1:x+2, [data_h-2,data_h-1,data_h-1]]
            output[x,data_h-1] = (cut * mask).sum()

        apply_filter_body(data, mask, output)
    
    out = np.zeros([bh,bw,bpp], dtype=int)

    for canal in range(bpp):
        apply_filter(np_array[:,:,canal], filter, out[:,:,canal])

    out = np.minimum(np.maximum(out, 0), 255)

    out = out.reshape(bw*bh*bpp,1)
    tmp_array = array.array('B', out)
    src_rgn[bx1:bx2, by1:by2] = tmp_array.tostring()
    drawable.flush()
    drawable.update(0, 0, image.width, image.height)
    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

register(
        "gaussian_blur_plugin",
        "Gaussian_blur",
        "Gaussian_blur",
        "Josef Struz",
        "@JS",
        "2017",
        "Gaussian Blur",
        "RGB*, GRAY*",
        [
            (PF_IMAGE, "image", "takes current image", None),
            (PF_DRAWABLE, "drawable", "Input layer", None),
        ],
        [],
        gaussian_blur_main, menu="<Image>/Filters/JS-Filters" )

main()