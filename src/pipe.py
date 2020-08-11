from scipy.ndimage import label, find_objects
import cv2 
import numpy as np
from img_preperation import img_quantize, img_blur, read_img
from spline import Spline
from outline import get_outline_points
from SVGBuilder import SVGBuilder
from copy import deepcopy
from trace import *


#TODO: not interpolate corner point
#TODO: refactor it on functions, maybe use multi-proc?

def pipe(img_path, colors_num=16, blur=True, max_pieces_size=0):

    img = cv2.imread(img_path)

    img = img_blur(img)
    img = img_quantize(img, 7)
    cols, rows, _ = img.shape

    svg = SVGBuilder()
    svg.create_canvas(width=rows, height=cols)

    outlines = trace(img)

    # We need to sort outlines, because one outline can cover other outline
    outlines = sorted(outlines, key=lambda elem: min(elem['outline_points']))
    for outline_obj in outlines:
        outline_points = outline_obj['outline_points']
        if len(outline_points) < 4:
            svg.add_poly_element(outline_points, outline_obj['fill'])
        else:
            outline_on_img = Spline.get_cubic_b_spline_points(np.array(outline_points))  
            svg.add_spline_element(outline_on_img, outline_obj['fill'])

    svg.save_as_svg('vot-eto-da-both.svg')


if __name__ == "__main__":
    pipe(img_path='img/vector.png', colors_num=8)
