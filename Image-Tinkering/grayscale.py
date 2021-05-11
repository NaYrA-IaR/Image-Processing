import numpy as np

# Grayscale Image is an image with only one value for a pixel which represents black, white or 253 shades of gray.

def convert_to_grayscale(data):

    
    row, column = data.shape[:2]
    new_data = np.zeros((row,column))
    
    for r in range(row):
        for c in range(column):
            new_data[r][c] = (data[r][c][0] + data[r][c][1] + data[r][c][2])/3 # Only taking RGB values out of the RGBA format.

    return new_data