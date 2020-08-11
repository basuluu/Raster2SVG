        outline_on_matrix.append(outline_on_matrix[0])
        for i, point in enumerate(outline_on_matrix):
            if i == len(outline_on_matrix)-1:
                break
            x1, y1 = outline_on_matrix[i]
            x2, y2 = outline_on_matrix[i+1]

            if y2 - y1 > 0:
                direction = 'down'
                point_1_neighbour = (y1+1, x1)
                point_2_neighbour = (y2-1, x2)
            elif y2 - y1 < 0:
                direction = 'up'
                point_1_neighbour = (y1-1, x1)
                point_2_neighbour = (y2+1, x2)
            elif x2 - x1 > 0:
                direction = 'right'
                point_1_neighbour = (y1, x1+1)
                point_1_neighbour = (y2, x2-1)
            else:
                direction = 'left'
                point_1_neighbour = (y1, x1-1)
                point_2_neighbour = (y2, x2+1)

            outline_with_shift.append(point)
            
            outline_with_shift.append(point_1_neighbour)
            outline_with_shift.append(point_2_neighbour)