import cv2
import numpy as np
from figure import Moore

from spline import Spline


def get_outline_points(item):
    (number, figure), label = item
    fig_matrix = figure.figure_matrix

    # if label == 'poly':
    #     countrs, _ = cv2.findContours(fig_matrix, cv2.cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    #     outline_on_matrix = list(zip(countrs[0].T[0][0], countrs[0].T[1][0]))
    countrs, _ = cv2.findContours(fig_matrix, cv2.cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    outline_on_matrix = list(zip(countrs[0].T[0][0], countrs[0].T[1][0]))
    # outline_on_matrix = Moore.get_moore_bounds(fig_matrix, 255)
    outline_on_img = figure.get_true_pixels(outline_on_matrix)
    outline_on_img.append(outline_on_img[0])
    
    if len(outline_on_img) <= 3:
        return (0, [], '', '')

    if label == 'poly' or len(outline_on_img) == 5:
        pass
    else:
        outline_on_img = Spline.get_cubic_b_spline_points(np.array(outline_on_img))

    return  (number, outline_on_img, label, figure.figure_color)