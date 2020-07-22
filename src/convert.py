import cv2
import numpy as np 
import multiprocessing

from figure import *
from SVGBuilder import SVGBuilder
from spline import Spline
from img_preperation import img_quantize, img_blur, read_img
from trace import trace
from outline import get_outline_points

from datetime import datetime
import time

# start_time = datetime.now()

def compress_matrix(item):
    number, figure = item
    return (number, figure.compress_figure_matrix())

def convert(img_path, colors_num=255, blur=True, max_pieces_size=0):
    
    img = read_img(img_path)
    img = img_blur(img) if blur else img
    img = img_quantize(img, colors_num)
    
    max_pieces_size = max_pieces_size

    rows, cols, _ = img.shape

    svg = SVGBuilder()
    svg.create_canvas(width=cols, height=rows)

    figure_lst = trace(img, max_pieces_size)

    with multiprocessing.Pool(3) as pool:
        figure_compressed_lst = sorted(list(pool.map(compress_matrix, figure_lst)))

    print(['circled']*len(figure_lst))
    ## TODO: Нужно изменить версию OPENCV, PYVENV нормально развернуть по человечи
    with multiprocessing.Pool(3) as pool:
        forms = sorted(list(pool.map(get_outline_points, zip(figure_lst, ['circled']*len(figure_lst)))))

    for (_, points, label, color) in forms:
        if not label:
            continue
        fill = f"rgb({','.join([str(pix) for pix in color])})"
        if label == 'circled':
            svg.add_spline_element(points, fill)
        else:
            svg.add_poly_element(points, fill)

    svg.save_as_svg('vot-eto-da-both.svg')


if __name__ == "__main__":

    convert('img/rect.png', colors_num=30, blur=True)

# print(datetime.now() - start_time)