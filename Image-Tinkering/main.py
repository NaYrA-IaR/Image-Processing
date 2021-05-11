from png_decoder import img
from matplotlib import pyplot as plt
from binarizer import binarize
from scaleup import scale
import numpy as np


image = img("image.png")

#binarizing image
threshold = 127
new_data = binarize(image, threshold)

#scaling image
new_data = np.array(scale(image, 0.5))

plt.imshow(new_data)
plt.show()
