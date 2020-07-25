from scipy.ndimage import label, find_objects
import cv2 
import numpy as np
from img_preperation import img_quantize, img_blur, read_img
from spline import Spline
from outline import get_outline_points
from SVGBuilder import SVGBuilder
from copy import deepcopy


img = cv2.imread('img/orel.jpg')
img = img_blur(img)
img = img_quantize(img, 2)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cols, rows = img.shape

svg = SVGBuilder()
svg.create_canvas(width=rows, height=cols)

outlines = []


for color in np.unique(img):
    ## Если color == 0, то он все зануляет и белый не ищет!
    img_copy = deepcopy(img)
    
    if color == 0:
        img_copy[img_copy!=color] = 0
        img_copy[img==color] = 1
    else:
        img_copy[img_copy!=color] = 0
    print(color, type(color))
    matrix, count = label(img_copy)

    matrix[matrix!=0] = 255
    matrix = matrix.astype('uint8')

# show_img(matrix.astype('uint8'))

    countrs, _ = cv2.findContours(matrix, cv2.cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    print(len(countrs))

    fill = f"rgb({','.join([str(color)]*3)})"

    for i in range(len(countrs)):    
        #countrs[0], countrs[1], countrs[2] и т.д.
        outline_on_matrix = list(zip(countrs[i].T[0][0], countrs[i].T[1][0]))
        
        if len(outline_on_matrix) < 3:
            continue

        outlines.append({
            'outline_points': outline_on_matrix,
            'fill': fill,
        })


outlines = sorted(outlines, key=lambda elem: min(elem['outline_points']))
for outline_obj in outlines:
    outline_on_img = Spline.get_cubic_b_spline_points(np.array(outline_obj['outline_points']))    
    svg.add_spline_element(outline_on_img, outline_obj['fill'])

svg.save_as_svg('vot-eto-new.svg')
