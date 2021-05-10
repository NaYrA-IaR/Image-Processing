from png_decoder import img
from matplotlib import pyplot as plt
from binarizer import binarize


image = img("../image.png")
threshold = 127
new_data = binarize(image, threshold)
plt.imshow(new_data)
plt.show()
