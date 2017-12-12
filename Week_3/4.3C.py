import random
import math

def sigmoid(x):
    return 1 / (1 + (math.e ** (-x)))

def derivativeSigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

class Perceptron:
    bias = -1

    def __init__(self, inputs, learnRate=0.5):
        # Add a bias
        self.input = inputs + [self.bias]
        self.weights = []

        for entry in self.input:
            self.weights.append(random.random())
        self.learnRate = learnRate

        self.sum = 0
        self.activation = 0

    def get_sum(self):
        self.sum = 0
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.sum += (self.input[i].get_activation() * self.weights[i])
            else:
                self.sum += self.input[i] * self.weights[i]
        return self.sum

    def get_error(self):
        return self.error

    def calc_error(self, error=None, weight=None, expectation=None):
        if error != None and expectation == None:
            self.error = derivativeSigmoid(self.activation) * weight * error
        elif expectation != None and error == None:
            self.error = derivativeSigmoid(self.sum) * (expectation - self.activation)
        else:
            print("Wrong function call on calc_error")
            print("Input you have given was error={} expectation={}".format(error, expectation))
            exit()
        return self.error

    def calc_nested_error(self, totalError):
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.input[i].calc_error(error=totalError, weight=self.weights[i])

    def update_weights(self):
        for i in range(len(self.input)):
            self.weights[i] += (self.learnRate * self.weights[i] * self.error)

    def set_input(self, input):
        # Minus one because of the bias
        if len(input) != len(self.input)-1:
            print("ERROR: The new input is not correct, either too many or too few points")
            print("New input", input)
            print("Current input", self.input)
            exit()
        else:
            # re-add the bias
            self.input = input + [self.bias]

    def get_activation(self):
        self.activation = sigmoid(self.get_sum())
        return self.activation

class Network:
    def __init__(self, network):
        self.network = list(reversed(network))  # Reverse so index 0 is output layer
        self.outputError = []

    def update(self, numbers):
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
        self.calc_output()
        return self.output

    def calc_output(self):
        reversedNetwork = list(reversed(self.network))  # Reverse so index 0 is first layer
        self.output = []
        for layer in reversedNetwork:
            if layer == reversedNetwork[-1]:
                for entry in layer:
                    self.output.append(entry.get_activation())
            else:
                for entry in layer:
                    entry.get_activation()



#######
# XOR #
#######
XORData =  [[[0,0], 0],
            [[0,1], 1],
            [[1,0], 1],
            [[1,1], 0]]
perceptron1 = Perceptron(XORData[0][0])
perceptron2 = Perceptron(XORData[0][0])
perceptron3 = Perceptron([perceptron1, perceptron2])
network = Network([[perceptron1, perceptron2], [perceptron3]])

for j in range(len(XORData)):
        perceptron1.set_input(XORData[j][0])
        perceptron2.set_input(XORData[j][0])
        print("input: {} activation: {} result: {}".format(XORData[j][0], network.get_output(), XORData[j][1]))

for i in range(100):
    for j in range(len(XORData)):
        perceptron1.set_input(XORData[j][0])
        perceptron2.set_input(XORData[j][0])
        network.update([XORData[j][1]])
    perceptron1.set_input(XORData[2][0])
    perceptron2.set_input(XORData[2][0])
    print("input: {} activation: {} result: {}".format(XORData[2][0], network.get_output(), XORData[2][1]))
print()

for j in range(len(XORData)):
        perceptron1.set_input(XORData[j][0])
        perceptron2.set_input(XORData[j][0])
        print("input: {} activation: {} result: {}".format(XORData[j][0], network.get_output(), XORData[j][1]))
