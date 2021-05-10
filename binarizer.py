from matplotlib import image 
from matplotlib import pyplot as plt

def binarize(data) :
    threshold = 128
    return (data > threshold)*255


image = image.imread("image.png")
from numpy import asarray
data = asarray(image)
new_data = binarise(image)
plt.imshow(new_data)
plt.show()
