import math, random, numpy as np

def sigmoid(x):
    return 1 / (1 + math.e ** (-x))

data = [[[0,0], 1],
        [[0,1], 0],
        [[1,0], 0],
        [[1,1], 0]]

theta = np.array([[random.random(), random.random()]])
bias = np.array([[random.random()]])
