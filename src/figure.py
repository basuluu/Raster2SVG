import cv2
import numpy as np 


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def coords(self):
        return self.x, self.y
    
    def clockwise(self):
        cl = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        return [Point(self.x + x, self.y + y) for x, y in cl]

    def next_clockwise(self, prev):
        # cl = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        # i = (cl.index((self - prev).coords()) + 1) % 8
        # x, y = cl[i]
        # return Point(self.x + x, self.y + y)
        return self.clockwise()[(self.clockwise().index(prev) + 1) % 8]


# По сути, буду использоватьб только get_moore_bounds для получения точек контура
class Moore:

    #
    # Нахождение контура методом мура по матрице из 0, 1
    # 0 - пустая зона, 1 - зона с фигурой
    # Возвращает список точек контура [(x1, y1), (x2, y2)]
    # fig - входная матрица 0, 1
    # prev - точка входа, как правило start - Point(1,0)
    # start - точка начала трассировки
    @staticmethod
    def moore_neighbor_trace(fig: "Matrix", prev: Point, start: Point, cl_value):
        contour = [start.coords()]

        current = start
        backtrack = prev
        considered = start.next_clockwise(prev)
        step = 0
        while considered != start:
            if step >= fig.size * 5:
                return contour
            step += 1
            try:
                point = fig[considered.y, considered.x]
                if point == cl_value:
                    contour.append(considered.coords())
                    backtrack = current
                    current = considered
                    considered = current.next_clockwise(backtrack)
                else:
                    backtrack = considered
                    considered = current.next_clockwise(backtrack)
            except:
                backtrack = considered
                considered = current.next_clockwise(backtrack)
        return contour
    
    #
    # Ищет точку вхождения, для начала трассировки контура
    # Получить контур фигуры fig
    # Возвращает список точек контура [(x1, y1), (x2, y2)]
    # fig - входная матрица 0, 1
    # cl_value - значение цвета фигуры, для которой ищем контур
    #
    @staticmethod
    def get_moore_bounds(fig: "Matrix", cl_value: int):
        rows, cols = fig.shape
        for x in range(cols):
            for y in range(rows):
                if fig[y, x] == cl_value:
                    outline = Moore.moore_neighbor_trace(fig, Point(x, y) - Point(1, 0), Point(x, y), cl_value)
                    return outline

class Figure:
    def __init__(self, img: cv2.imread, start_pixel: tuple):
        self.img = img
        self.rows, self.cols, _ = img.shape
        self.start_pixel = start_pixel      # Пиксель, с которого начинаем путь
                
        self.figure_pixels = set()
        self.figure_color = self.get_pixel_color(self.start_pixel)

        self.figure_matrix = None

        
    def get_pixel_color(self, pixel):
        return self.img[pixel]
        
    def is_exist_pixel(self, pixel):
        i, j = pixel
        if i < 0 or i >= self.rows:
            return False
        elif j < 0 or j >= self.cols:
            return False
        return True
    
    def is_same_color(self, pixel):
        pixel_color = self.get_pixel_color(pixel)
        if np.equal(pixel_color, self.figure_color).all():
            return True 
        return False
    
    def create_figure(self):
        pixels_to_check = set()
        pixels_was_checked = set()

        pixels_to_check.add(self.start_pixel)
        
        while len(pixels_to_check) > 0:
            pixel = pixels_to_check.pop()
            if pixel in pixels_was_checked:
                continue

            pixels_was_checked.add(pixel)
            
            i, j = pixel

            if not self.is_exist_pixel(pixel):
                continue
            
            elif not self.is_same_color(pixel):
                continue
            
            pixels_to_check.add((i+1, j))
            pixels_to_check.add((i-1, j))
            pixels_to_check.add((i, j+1))
            pixels_to_check.add((i, j-1))
            
            self.figure_pixels.add((i, j))
            
    def get_figure_pixels(self):
        return self.figure_pixels
    
    # -> добавил справа и снизу заполнение единницами
    # нужно для правильной обводки. Объясняется это так,
    # для двух пикселей строится всего 1 клетка на координатах
    # для трех пикселей строится всего 2 клетки на координатах
    # поэтому избыточность в виде +1 по rows, cols оправдана.
    def create_figure_matrix(self):
        rows_max = max([y for y, x in self.figure_pixels])
        rows_min = min([y for y, x in self.figure_pixels])
        cols_max = max([x for y, x in self.figure_pixels])
        cols_min = min([x for y, x in self.figure_pixels])
        
        rows = rows_max - rows_min
        cols = cols_max - cols_min
        
        # Увеличил до 3-ех чтобы добавить пустые границы из 0
        # Увеличил до 4-ех чтобы добавить пустые границы из 0 и добавить единницы снизу-справа

        matrix = np.zeros((rows+4, cols+4), dtype='uint8')
        for pixel in self.figure_pixels:
            i, j = pixel
            
            i_pos = i - rows_min + 1
            j_pos = j - cols_min + 1
            
            if (i+1, j) not in self.figure_pixels and (i, j+1) not in self.figure_pixels:
                matrix[i_pos+1, j_pos] = 255
                matrix[i_pos, j_pos+1] = 255
                matrix[i_pos+1, j_pos+1] = 255
            elif (i+1, j) not in self.figure_pixels:
                matrix[i_pos+1, j_pos] = 255
            elif (i, j+1) not in self.figure_pixels:
                matrix[i_pos, j_pos+1] = 255
            
            matrix[i_pos, j_pos] = 255
        self.figure_matrix = matrix
                
    def compress_figure_matrix(self):
        if self.figure_matrix is None:
            raise IndexError
        rows, cols = self.figure_matrix.shape
        if rows > 50 or cols > 50:
            return cv2.resize(self.figure_matrix, (50,50)).flatten()
        zero = np.zeros((50,50), np.uint8)
        zero[:rows,:cols] = self.figure_matrix
        return zero.flatten()

    # Нужно для восстановления стартовых позиций пикселей на изображение, а не в матрице
    def get_skip_cols(self):
        return min([x for y, x in self.figure_pixels]) - 1
    
    def get_skip_rows(self):
        return min([y for y, x in self.figure_pixels]) - 1
    
    # outline, результат обводки мура
    def get_true_pixels(self, outline):
        base_col = self.get_skip_cols()
        base_row = self.get_skip_rows()
        return [(x + base_col, y + base_row) for x, y in outline]