from scipy.ndimage import label
import cv2
import numpy as np

from copy import deepcopy


# TODO: think about corners of not rectangle figure
# TODO: still have bug of white lines beside figures

def trace(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    outlines = []
    for color in np.unique(img_gray):
        bw_mask = get_image_bw_mask(img_gray, color)
        outlines += get_outline(img, bw_mask)
    return outlines

# Create black and white mask, where black(255) is group of pixels with searched color
def get_image_bw_mask(img_gray, color):
    color_mask = deepcopy(img_gray)
    # If color == 0, we need to invert (0 -> 1) and (other colors -> 0)
    if color == 0:
        color_mask = color_mask * 0
        color_mask[img_gray==color] = 255
    else:
        color_mask[color_mask!=color] = 0
        color_mask[color_mask==color] = 255
    return color_mask.astype('uint8')

def get_outline(img, bw_mask):
    fill = None
    outlines = []
    # search countrs and approx it
    # need two approx groups for collect corner points with closes neigbors
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

        corners_with_neighbor_points = collect_neighbor_corner_points(
            countr_approx_points, countr_full_points
        )

        if fill == None:
            index = (corners_with_neighbor_points[0][1], corners_with_neighbor_points[0][0])
            fill = get_fill_color(img, index)

        outlines.append({
            'outline_points': corners_with_neighbor_points,
            'fill': fill,
        })
    return outlines

# get corner points with closes neighbor
# return list of coords [(0,0), (0, 1)...(1, 0)]
# [[1, 1, 1, 1, 1],          [[1, 1, 0, 1, 1],
#  [1, 1, 1, 1, 1],    <->    [1, 0, 0, 0, 1],
#  [1, 1, 1, 1, 1],    <->    [1, 0, 0, 0, 1],
#  [1, 1, 1, 1, 1]]           [1, 1, 0, 1, 1]]
def collect_neighbor_corner_points(countr_approx_points, countr_full_points):
    neighbor_corner_points = []
    for point in countr_approx_points:
        index = countr_full_points.index(point)
        if index == 0:
            neighbor_corner_points.append(point)
            neighbor_corner_points.append(countr_full_points[1])
        else:
            neighbor_corner_points += countr_full_points[index-1:index+2]
        # Close our contour for last dot
        if point == countr_approx_points[-1]:
            neighbor_corner_points.append(countr_full_points[-1])
            neighbor_corner_points.append(countr_approx_points[0])

        countr_full_points = countr_full_points[index+1:]  
    return neighbor_corner_points

# return value of svg fill attribute
def get_fill_color(img, index):
    red, green, blue = img[index] 
    return f"rgb({red}, {green}, {blue})"