import numpy as np
from scipy import interpolate

# Spline.get_cubic_b_spline_points(points) -> вернет точки б-сплайна
# out = [(x1,y1),(x2,y2)]
class Spline:
    # Возвращает список точек б-сплайна, [(x1,y1),(x2,y2)]
    @staticmethod
    def get_cubic_b_spline_points(points: np.array, optimization=True) -> list:
        x = points[:,0]
        y = points[:,1]

        points_num = len(x)  

        # Создаем узлы
        t = np.linspace(0, 1, points_num-2, endpoint=True)
        t = np.append([0,0,0], t)
        t = np.append(t, [1,1,1])
        
        tck = [t, [x, y], 3] #knots, coefficients, and degree of the spline

        u3 = np.linspace(0, 1, points_num*2, endpoint=True)
        out = interpolate.splev(u3, tck)

        if optimization:
            out = [reduce_points_len(array) for array in out]

        return list(zip(out[0], out[1]))


# Округлить, уменьшить число знаков после запятой.
def reduce_points_len(array: np.array):
    return np.around(array, decimals=2)