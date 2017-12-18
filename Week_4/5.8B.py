import math, random, numpy as np


def sigmoid(x):
    return 1 / (1 + math.e ** (-x))


def predict(x, theta):
    prediction = None
    for weight in theta:
        if prediction == None:
            prediction = sigmoid(np.dot(weight, x))
        else:
            prediction = sigmoid(np.dot(weight, prediction))
    return prediction


data = [[[1, 0, 0], 1],
        [[1, 0, 1], 0],
        [[1, 1, 0], 0],
        [[1, 1, 1], 0]]

theta1 = np.array([[random.random(), random.random(), random.random()]])

print(predict(data[0][0], theta1))
