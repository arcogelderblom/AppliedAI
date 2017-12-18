import os, gzip, pickle, numpy as np

from urllib import request
from matplotlib import cm
from matplotlib.pyplot import imshow, show

url = "http://deeplearning.net/data/mnist/mnist.pkl.gz"
if not os.path.isfile("Dataset/mnist.pkl.gz"):
    request.urlretrieve(url, "Dataset/mnist.pkl.gz")

f = gzip.open('Dataset/mnist.pkl.gz', 'rb')
train_set , valid_set , test_set = pickle.load(f, encoding='latin1')
f.close()

def get_image(number):
    (X, y) = [img[number] for img in train_set]
    return (np.array(X), y)


def view_image(number):
    (X, y) = get_image(number)
    print("Label: %s" % y)
    imshow(X.reshape(28,28), cmap=cm.gray)
    show()
view_image(0)
