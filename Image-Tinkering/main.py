from png_decoder import img
from matplotlib import pyplot as plt
from binarizer import binarize
from scaleup import scale
import numpy as np
from grayscale import convert_to_grayscale 


image = img("image.png")

#binarizing image
threshold = 127
binarized_image = binarize(image, threshold)

#scaling image
scaled_image = np.array(scale(image, 0.5))

# Grayscale Image
gray_image = convert_to_grayscale(image)

plt.imshow(gray_image, cmap="gray")
plt.show()
