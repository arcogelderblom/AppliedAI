import os, gzip, pickle, numpy as np
from math import e
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

convertTable= {1: np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
               2: np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
               3: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
               4: np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
               5: np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
               6: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
               7: np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
               8: np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
               9: np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
               0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])}

def sigmoid(x):
    """Standard sigmoid; since it relies on ** to do computation, it broadcasts on vectors and matrices"""
    return 1 / (1 - (e**(-x)))

def derivative_sigmoid(x):
    """Expects input x to be already sigmoid-ed"""
    return x * (1 - x)

def tanh(x):
    """Standard tanh; since it relies on ** and * to do computation, it broadcasts on vectors and matrices"""
    return (1 - e ** (-2*x))/ (1 + e ** (-2*x))

def derived_tanh(x):
    """Expects input x to already be tanh-ed."""
    return 1 - tanh(x)


def forward(inputs,weights,function=sigmoid,step=-1):
    """Function needed to calculate activation on a particular layer.
    step=-1 calculates all layers, thus provides the output of the network
    step=0 returns the inputs
    any step in between, returns the output vector of that particular (hidden) layer"""
    if step == 0:
        return inputs
    elif step == -1:
        step = len(weights)
        return function(np.dot(weights[step-1], np.append(1, forward(inputs, weights, function, step-1))))
    else:
        if step == len(weights):
            return function(np.dot(weights[step-1], np.append(1, forward(inputs, weights, function, step-1))))
        else:
            return function(np.dot(weights[step-1], np.append(1, forward(inputs, weights, function, step-1))))


def backprop(inputs, outputs, weights, function=sigmoid, derivative=derivative_sigmoid, eta=0.01):
    """
    Function to calculate deltas matrix based on gradient descent / backpropagation algorithm.
    Deltas matrix represents the changes that are needed to be performed to the weights (per layer) to
    improve the performance of the neural net.
    :param inputs: (numpy) array representing the input vector.
    :param outputs:  (numpy) array representing the output vector.
    :param weights:  list of numpy arrays (matrices) that represent the weights per layer.
    :param function: activation function to be used, e.g. sigmoid or tanh
    :param derivative: derivative of activation function to be used.
    :param learnrate: rate of learning.
    :return: list of numpy arrays representing the delta per weight per layer.
    """
    inputs = np.array(inputs)
    outputs = np.array(outputs)
    deltas = []
    layers = len(weights) # set current layer to output layer
    a_now = forward(inputs, weights, function, layers) # activation on current layer
    for i in range(0, layers):
        a_prev = forward(inputs, weights, function, layers-i-1) # calculate activation of previous layer
        if i == 0:
            error = np.array(derivative(a_now) * (outputs - a_now))  # calculate error on output
        else:
            error = derivative(a_now) * (weights[-i].T).dot(error)[1:] # calculate error on current layer
        delta = eta * np.expand_dims(np.append(1, a_prev), axis=1) * error # calculate adjustments to weights
        deltas.insert(0, delta.T) # store adjustments
        a_now = a_prev # move one layer backwards

    return deltas

# Layer 10 neurons, each representing a digit in the range 0...9, with inputs, each representing 1 pixel plus 1 because of a bias
theta1 = np.random.rand(10, 785)

w = [theta1]
tmp = forward(get_image(0)[0], w)

for train in range(1):
    for i in range(len(train_set[0])):
        input = get_image(i)[0]
        output = convertTable[get_image(i)[1]]
        deltas = backprop(input, output, w)
        for index in range(len(w)):
            w[index] = w[index] + deltas[index]

if tmp.all() == forward(get_image(0)[0], w).all():
    print("Training did not change anything")
