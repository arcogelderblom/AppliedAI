import random
import math
import numpy as np


def sigmoid(x):
    return 1 / (1 + (math.e ** (-x)))


def derivativeSigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


class Perceptron:
    """
    Perceptron class
    """
    bias = -1

    def __init__(self, inputs, learnRate=0.5):
        """
        :param inputs: list of inputs of the Perceptron
        :param learnRate: learn rate necessary for some calculation, standard is 0.5
        """
        # Add a bias
        self.input = inputs + [self.bias]
        self.weights = []

        for entry in self.input:
            self.weights.append(random.uniform(-2, 2))

        self.learnRate = learnRate

        self.sum = 0
        self.activation = 0

    def get_sum(self):
        """
        :return returns the weighted sum
        """
        self.sum = 0
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.sum += (self.input[i].get_activation() * self.weights[i])
            else:
                self.sum += self.input[i] * self.weights[i]
        return self.sum

    def get_error(self):
        """
        :return: returns an value for error
        """
        return self.error

    def calc_error(self, error=None, weight=None, expectation=None):
        """
        Calculate the error, either give a value to expectation or an value to weight and error.
        :param error: the total error of the layer before
        :param weight: weight of the connection between output and input
        :param expectation: expected outcome
        :return: the calculated error
        """
        if error != None and weight != None and expectation == None:
            self.error = derivativeSigmoid(self.sum) * weight * error
        elif expectation != None and weight == None and error == None:
            self.error = derivativeSigmoid(self.sum) * (expectation - self.activation)
        else:
            print("Wrong function call on calc_error")
            print("Input you have given was error={} weight={} expectation={}".format(error, weight, expectation))
            exit()
        return self.error

    def calc_nested_error(self, totalError):
        """
        Calculate the error of all inputs using the total error and the weight belonging to the correct input
        :param totalError: the total error of the layer before
        """
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.input[i].calc_error(error=totalError, weight=self.weights[i])

    def update_weights(self):
        """
        Update all the weights of the Perceptrons inputs
        """
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.weights[i] += (self.learnRate * self.input[i].activation * self.error)
            else:
                self.weights[i] += (self.learnRate * self.input[i] * self.error)

    def set_input(self, input):
        """
        Sets new input values without changing the weights, usefull for training purposes. Note that a bias does not
        need to be included, the bias is added automatically.
        :param input: list of inputs without a bias
        """
        # Minus one because of the bias
        if len(input) != len(self.input) - 1:
            print("ERROR: The new input is not correct, either too many or too few points")
            print("New input", input)
            print("Current input", self.input)
            exit()
        else:
            # re-add the bias
            self.input = input + [self.bias]

    def get_activation(self):
        """
        :return: The calculated activation value
        """
        self.activation = sigmoid(self.get_sum())
        return self.activation


class Network:
    """
    Network class
    """

    def __init__(self, network):
        """
        Initialize a network using a list of lists where the total list is the network, and the nested lists represent
        layers like this: [ [layer1], [layer2] ]
        :param network: list of lists containing Perceptrons
        """
        self.network = list(reversed(network))  # Reverse so index 0 is output layer
        self.outputError = []

    def update(self, numbers):
        """
        :param numbers: list of expectations
        """
        if len(numbers) != len(self.network[0]):
            print("Your expected amount of outputs is not equal to the amount of neurons in the last layer")
            exit()
        else:
            self.calc_output()  # First go through the network to set correct sum and activation settings
            self.calc_network_error(numbers)
            for layer in self.network:
                for entry in layer:
                    entry.update_weights()

    def calc_network_error(self, numbers):
        """
        Go through the network to calculate it's all error values
        :param numbers: list of expectation
        """
        self.outputError = []
        for i in range(len(self.network)):
            if i == 0:
                error = 0
                for j in range(len(self.network[i])):
                    error += self.network[i][j].calc_error(expectation=numbers[j])
                self.outputError.append(error)
            else:
                if i + 1 == len(self.network):
                    for entry in self.network[i - 1]:
                        entry.calc_nested_error(self.outputError[i - 1])
                else:
                    error = 0
                    for entry in self.network[i - 1]:
                        entry.calc_nested_error(self.outputError[i - 1])
                    for entry in self.network[i]:
                        error += entry.get_error()
                    self.outputError.append(error)

    def get_output(self):
        """
        :return: the calculated output of the nework
        """
        self.calc_output()
        return self.output

    def calc_output(self):
        """
        Calculate the output of the network. This is stored in a list variable.
        """
        reversedNetwork = list(reversed(self.network))  # Reverse so index 0 is first layer
        self.output = []
        # The get activation looks to own layer and layer before, so skip first layer and stop at last layer
        for layer in reversedNetwork:
            if layer == reversedNetwork[0]:
                continue
            elif layer == reversedNetwork[-1]:
                for entry in layer:
                    self.output.append(entry.get_activation())
            else:
                for entry in layer:
                    entry.get_activation()


# Data used for training is all data except for the last 3 of every flowertype, this is used for testing
equivalents = {"Iris-setosa": [1, 0, 0],
               "Iris-versicolor": [0, 1, 0],
               "Iris-virginica": [0, 0, 1],}

# Import training data
data = np.genfromtxt('Dataset/bezdekIris.data.txt', delimiter=',', usecols=[0, 1, 2, 3]).tolist()
tmpTypes = np.genfromtxt('Dataset/bezdekIris.data.txt', dtype=str, delimiter=',', usecols=[4])

types = []
for flowerType in tmpTypes:
    types.append(equivalents[flowerType])

# Import test data
testData = np.genfromtxt('Dataset/bezdekIris.testData.txt', delimiter=',', usecols=[0, 1, 2, 3]).tolist()
testTmpTypes = np.genfromtxt('Dataset/bezdekIris.testData.txt', dtype=str, delimiter=',', usecols=[4])

testTypes = []
for flowerType in testTmpTypes:
    testTypes.append(equivalents[flowerType])
learnrate = 0.7
# The network setup
layer1_1 = Perceptron([0, 0, 0, 0], learnrate)
layer1_2 = Perceptron([0, 0, 0, 0], learnrate)
layer1_3 = Perceptron([0, 0, 0, 0], learnrate)
layer1_4 = Perceptron([0, 0, 0, 0], learnrate)

# 4 inputs, for every distinctive property 1
layer1 = [layer1_1, layer1_2, layer1_3, layer1_4]

output_1 = Perceptron(layer1, learnrate)
output_2 = Perceptron(layer1, learnrate)
output_3 = Perceptron(layer1, learnrate)

# 3 outputs for the possible 3 answers
outputlayer = [output_1, output_2, output_3]

network = Network([layer1, outputlayer])

trainingAmount = 20000
for j in range(trainingAmount):
    print(j)
    for i in range(len(data)):
        for perceptron in layer1:
            perceptron.set_input(data[i])
        network.update(types[i])

for i in range(len(testData)):
    for perceptron in layer1:
        perceptron.set_input(testData[i])
    tmp = network.get_output()

    print(testData[i])
    for result in range(len(tmp)):
        print(testTypes[i][result], tmp[result])
    print()

"""
Using 2 layers, 4 perceptrons in first layer and 3 perceptrons in second layer
After 20000 training cycles this is the result: very good in recognizing 2 flowers, sucks at the other.
    [4.6, 3.2, 1.4, 0.2]
    1 0.9999474017349969
    0 0.00463060774660794
    0 6.097374143674061e-20

    [5.3, 3.7, 1.5, 0.2]
    1 0.9999477048870187
    0 0.00461342180909956
    0 6.077745206280764e-20

    [5.0, 3.3, 1.4, 0.2]
    1 0.9999475868371107
    0 0.004620111245462931
    0 6.085370490957907e-20

    [6.2, 2.9, 4.3, 1.3]
    0 3.828661916927722e-12
    1 0.9999999257324264
    0 2.0033850582385063e-10

    [5.1, 2.5, 3.0, 1.1]
    0 2.348258758220833e-13
    1 0.9999999970975888
    0 1.4197243846800672e-10

    [5.7, 2.8, 4.1, 1.3]
    0 1.467980066472219e-11
    1 0.9999996940698438
    0 1.9559945326926964e-10

    [6.5, 3.0, 5.2, 2.0]
    0 0.0007414501161123253
    0 0.024304156496187057
    1 1.4398280496890573e-10

    [6.2, 3.4, 5.4, 2.3]
    0 0.0012325815945438338
    0 0.014363712983638338
    1 1.4271698168523395e-10

    [5.9, 3.0, 5.1, 1.8]
    0 0.0007329576779295607
    0 0.024593908088825472
    1 1.440114885666432e-10

Using 2 layers, 8 perceptrons in first layer and 3 perceptrons in second layer
After 20000 training cycles this is the result: very good in recognizing 2 flowers, sucks at the other.
"""
