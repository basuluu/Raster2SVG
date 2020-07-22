import cairosvg
import random


class SVGBuilder:
    
    path_op = {'L': 1, 'S': 2, 'Q': 2, 'T': 1}
    
    def __init__(self):
        self.svg = ""
        self.svg_elements = []

        self.width = None
        self.height = None

    def create_canvas(self, width, height, background_color='white'):
        self.width = width - 1
        self.height = height - 1
        self.svg = '<?xml version="1.0" standalone="no"?>\n' \
                   '<svg xmlns="http://www.w3.org/2000/svg" '  \
                  f'viewBox="0 0 {self.width} {self.height}" version="1.1">'
        self.add_rect_element(width=width, height=height, fill=background_color)

    def add_rect_element(self, start_coord=(0,0), width=10, height=10, fill='black'):
        x, y = start_coord
        self.svg_elements.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}"/>'
        )
    
    def add_circle_element(self, center_coord=(0,0), radius=10, fill='black'):
        x, y = center_coord
        self.svg_elements.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" />'
        )

    def add_spline_element(self, points: list, fill='black'):
        x_prev, y_prev = None, None
        for x, y in points:
            if x_prev == None:
                spline_points = f"M {x} {y} "
                x_prev, y_prev = x, y
                continue
            spline_points += f"Q {x_prev}  {y_prev} {x} {y} "
            x_prev, y_prev = x, y
        self.svg_elements.append(f'<path d="{spline_points}" fill="{fill}"/>')

    def add_poly_element(self, points: list, fill='black'):
        poly_points = ' '.join([f"{x},{y}" for x,y in points])
        self.svg_elements.append(f'<polygon points="{poly_points}" fill="{fill}"/>')
                    
    def add_random_figure(self, points_num: int, fill='black'):
        if points_num < 3:
            return
        
        fp_x, fp_y = self.gen_random_coord()
        figure = f"M {fp_x} {fp_y} "
        
        for i in range(points_num):
            path_type = random.choice(list(self.path_op.keys()))
            figure += path_type
            for j in range(self.path_op[path_type]):
                x, y = self.gen_random_coord()
                figure += f" {x} {y} "
        figure += "z"
        self.svg_elements.append(f'<path d="{figure}" fill="{fill}"/>')
        
    def gen_random_coord(self):
        return (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def get_svg_text(self):
        return self.svg + ' '.join(self.svg_elements) + '</svg>'
    
    def save_as_svg(self, path):
        with open(path, 'w') as f:
            f.write(self.get_svg_text())
            
    def save_as_png(self, path):
        cairosvg.svg2png(bytestring=self.get_svg_text(), write_to=path)
            


            