from scipy.ndimage import label, find_objects
import cv2 
import numpy as np
from img_preperation import img_quantize, img_blur, read_img
from spline import Spline
from outline import get_outline_points
from SVGBuilder import SVGBuilder
from copy import deepcopy


#TODO: refactor it on functions, maybe use multi-proc?
img = cv2.imread('img/orel.jpg')
img = img_blur(img)
img = img_quantize(img, 2)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cols, rows = img.shape

svg = SVGBuilder()
svg.create_canvas(width=rows, height=cols)

outlines = []


for color in np.unique(img):

    # Create mask for our img/color -> [[0, 0, color, color, 0, 0]]
    img_copy = deepcopy(img)
    
    # If color == 0, we need to invert (0 -> 1) and (other colors -> 0)
    if color == 0:
        img_copy[img_copy!=color] = 0
        img_copy[img==color] = 1
    else:
        img_copy[img_copy!=color] = 0

    # search group of neighbour pixels, [0,1,1,0,1,1,0] -> [0,1,1,0,2,2,0]
    matrix, count = label(img_copy)

    # create black and white mask, where black(255) is group of pixels with searched color
    matrix[matrix!=0] = 255
    matrix = matrix.astype('uint8')

    # search countrs and approx it
    countrs, _ = cv2.findContours(matrix, cv2.cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    print(len(countrs))

    #TODO: need to fix color generation and get it from start img
    fill = f"rgb({','.join([str(color)]*3)})"

    # collect outline objects 
    for i in range(len(countrs)):    
        #countrs[0], countrs[1], countrs[2] и т.д., list[(x1, y1), (x2, y2), (x3, y3)]
        outline_on_matrix = list(zip(countrs[i].T[0][0], countrs[i].T[1][0]))
        

        # TODO: need to think how add row, col with ones to groups of pixel
        # cause this problem is actual,
        # [[1]] -> its one point in vector, but true is that it square that consist of 4 points
        # [[1, 1]]
        # [[1, 1]] -> look that i need from 1 square of pixel

        # if was only 1-2 pixels outline size will be 1-2 pixels,
        # its to low for get_cubic_b_spline_points
        if len(outline_on_matrix) < 3:
            continue

        outlines.append({
            'outline_points': outline_on_matrix,
            'fill': fill,
        })

# We need to sort outlines, because one outline can cover other outline
outlines = sorted(outlines, key=lambda elem: min(elem['outline_points']))
for outline_obj in outlines:
    outline_on_img = Spline.get_cubic_b_spline_points(np.array(outline_obj['outline_points']))    
    svg.add_spline_element(outline_on_img, outline_obj['fill'])

svg.save_as_svg('vot-eto-new.svg')
