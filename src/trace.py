from scipy.ndimage import label, find_objects
import cv2

from copy import deepcopy

from figure import *


# TODO: create function to get contour fill color
# TODO: think about corners of not rectangle figure
# TODO: still have bug of white lines beside figures

def trace(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    outlines = []
    for color in np.unique(img_gray):
        color_mask = get_image_color_mask(img_gray, color)
        # search group of neighbour pixels, [0,1,1,0,1,1,0] -> [0,1,1,0,2,2,0]
        matrix, count = label(color_mask)
        bw_mask = get_bw_mask(matrix)

        outlines += get_outline(img, bw_mask)
    return outlines

# Create mask for our img/color -> [[0, 0, color, color, 0, 0]]
def get_image_color_mask(img_gray, color):
    color_mask = deepcopy(img_gray)
    # If color == 0, we need to invert (0 -> 1) and (other colors -> 0)
    if color == 0:
        color_mask = color_mask * 0
        color_mask[img_gray==color] = 1
    else:
        color_mask[color_mask!=color] = 0
    return color_mask

# create black and white mask, where black(255) is group of pixels with searched color
def get_bw_mask(matrix):
    matrix[matrix!=0] = 255
    return matrix.astype('uint8')

def get_outline(img, bw_mask):
    fill = None
    outlines = []
    # search countrs and approx it
    countrs_approx, _ = cv2.findContours(bw_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    countrs_full, _   = cv2.findContours(bw_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # collect outline objects 
    for i in range(len(countrs_approx)):
        #countrs[0], countrs[1], countrs[2] и т.д., list[(x1, y1), (x2, y2), (x3, y3)]
        #but image pixel is img[y, x]

        countr_approx_points = list(zip(countrs_approx[i].T[0][0], countrs_approx[i].T[1][0]))
        countr_full_points   = list(zip(countrs_full[i].T[0][0], countrs_full[i].T[1][0]))

        if len(countr_approx_points) < 3:
            continue

        outline_on_matrix = []
        for point in countr_approx_points:
            index = countr_full_points.index(point)

            if index == 0:
                outline_on_matrix.append(point)
                outline_on_matrix.append(countr_full_points[1])
            else:
                outline_on_matrix += countr_full_points[index-1:index+2]

            # Close our contour for last dot
            if point == countr_approx_points[-1]:
                outline_on_matrix.append(countr_full_points[-1])
                outline_on_matrix.append(countr_approx_points[0])

            countr_full_points = countr_full_points[index+1:]            

        red, green, blue = img[outline_on_matrix[0][1], outline_on_matrix[0][0]] 
        fill = f"rgb({red}, {green}, {blue})"

        outlines.append({
            'outline_points': outline_on_matrix,
            'fill': fill,
        })
    return outlines
