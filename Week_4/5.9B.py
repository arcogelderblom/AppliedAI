import os, gzip, pickle, numpy as np

from urllib import request

url = "http://deeplearning.net/data/mnist/mnist.pkl.gz"
if not os.path.isfile("Dataset/mnist.pkl.gz"):
    request.urlretrieve(url, "Dataset/mnist.pkl.gz")

f = gzip.open('Dataset/mnist.pkl.gz', 'rb')
train_set , valid_set , test_set = pickle.load(f, encoding='latin1')
f.close()

def get_image(number):
    (X, y) = [img[number] for img in train_set]
    return (np.array(X), y)

convertTable= {1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               2: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               3: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               4: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               5: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               6: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
               7: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               8: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               9: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}


# First layer 784 neurons, each representing 1 pixel
# Last layer 10 neurons, each representing a digit in the range 0...9
