import numpy as np
import matplotlib.pyplot as plt

'''
 Reduce number of graylevels to a certain value, so that we have that many shades of gray.
 For reducing, we used the octile method, in which we find the number of weight as per given number of gray levels required.
 Then, matched the number of gray levels to that particular value and changed it to the values as we got from the octiles.
 E.g. If the value of a particular octile was say x and another was y, then we changed the value of a given pixel to that of x.
 This is how we reduced the number of gray levels.
'''


def graylevels(img, levels):
    dict = {}
    for y in img:
        for x in y:
            if x not in dict.keys(): 
                dict[x] = 1
            else:
                dict[x] += 1

    x = list(dict.keys())
    y = list(dict.values())

    x = x[1: len(x) - 1]
    y = y[1: len(y) - 1]

    xy = sorted([x, y])

    cf = [0]
    for i in y:
        i = i + cf[-1]
        cf.append(i)

    N = cf[-1]
    lev = 8
    tiles = []
    for i in range(1, lev):
        tile = i * N / 8
        for j in cf:
            if j >= tile:
                tile = j
                break
        tiles.append(xy[0][cf.index(tile)-1])
    
    tiles.sort()

    for yi, y in enumerate(img[:]):
        for xi, x in enumerate(y[:]):
            i = x
            j = 0
            
            if int(i) in range(0, int(tiles[0])):
                img[yi][xi] = np.float64(0)
            elif int(i) in range(int(tiles[0]), int(tiles[1])):
                img[yi][xi] = tiles[0]
            elif int(i) in range(int(tiles[1]), int(tiles[2])):
                img[yi][xi] = tiles[1]
            elif int(i) in range(int(tiles[2]), int(tiles[3])):
                img[yi][xi] = tiles[2]
            elif int(i) in range(int(tiles[3]), int(tiles[4])):
                img[yi][xi] = tiles[3]
            elif int(i) in range(int(tiles[4]), int(tiles[5])):
                img[yi][xi] = tiles[4]
            elif int(i) in range(int(tiles[5]), int(tiles[6])):
                img[yi][xi] = tiles[5]
            else:
                img[yi][xi] = np.float64(255)


    print(tiles)
    return img