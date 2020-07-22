from figure import *


def trace(img: np.array, max_pieces_size: int):
    rows, cols, _ = img.shape
    n = 0
    history = set()
    figure_lst = []
    for i in range(rows):
        for j in range(cols):
            if (i,j) in history:
                continue

            figure = Figure(img, (i,j))
            figure.create_figure()
            pixels = figure.get_figure_pixels()
            history.update(pixels)

            if len(pixels) < max_pieces_size:
                continue
                    
            figure.create_figure_matrix()
            figure_lst.append((n, figure))
            n += 1
    return figure_lst