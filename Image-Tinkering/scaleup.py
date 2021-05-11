import numpy as np

def scale(data, factor=2):
    new_data = list()
    row, column = data.shape[:2] 
    new_width = int(row*factor)
    new_height = int(column*factor)
    for r in range(new_width):
        temp = []
        for c in range(new_height):
            temp.append(data[int(row*r/new_width)][int(column*c/new_height)])

        new_data.append(temp)

    return new_data

