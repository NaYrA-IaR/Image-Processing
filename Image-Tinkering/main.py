from png_decoder import img
from matplotlib import pyplot as plt
from binarizer import binarize
from scaleup import scale
import numpy as np
from graylevel import graylevels
from grayscale import convert_to_grayscale 


image = img("image.png")

# Binarizing image
threshold = 127
binarized_image = binarize(image, threshold)

# Scaling image
scaled_image = np.array(scale(image, 0.5))

# Grayscale Image
gray_image = convert_to_grayscale(image)
print(gray_image.shape)

# Grayleveling the image
graylevel_image = graylevels(gray_image, 8)

plt.imshow(graylevel_image, cmap='gray')
plt.show()
