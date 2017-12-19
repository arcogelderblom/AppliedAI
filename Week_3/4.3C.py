import random
import math

def sigmoid(x):
    return 1 / (1 + (math.e ** (-x)))

def derivativeSigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

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
            self.weights.append(random.uniform(-2,2))

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

    def calc_error(self, error=None, expectation=None):
        """
        Calculate the error, either give a value to expectation or an value to weight and error.
        :param error: the total error of the layer before
        :param expectation: expected outcome
        :return: the calculated error
        """
        if error != None and expectation == None:
            self.error = derivativeSigmoid(self.sum) * error
        elif expectation != None and error == None:
            self.error = derivativeSigmoid(self.sum) * (expectation - self.activation)
        else:
            print("Wrong function call on calc_error")
            print("Input you have given was error={} expectation={}".format(error, expectation))
            exit()
        return self.error

    def get_error_per_layer(self):
        """
        Calculate for each input of the perceptron the 'error', being the error times the weight of the connection
        :return: list of errors, 1 entry per input
        """
        errors = []
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                errors.append(self.error * self.weights[i])
        return errors

    def calc_nested_error(self, errors):
        """
        Calculate the error of all inputs using the error belonging to the correct input
        :param errors: a list of errors to use for the calculation per input
        """
        for i in range(len(self.input)):
            if type(self.input[i]) is Perceptron:
                self.input[i].calc_error(error=errors[i])

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
        if len(input) != len(self.input)-1:
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
        for i in range(len(self.network)):
            if i == 0:
                for j in range(len(self.network[i])):
                    self.network[i][j].calc_error(expectation=numbers[j])
            else:
                error = []
                for entry in self.network[i - 1]:
                    if error == []:
                        error = entry.get_error_per_layer()
                    else:
                        tmp = error
                        error = [x + y for x, y in zip(tmp, entry.get_error_per_layer())]
                for entry in self.network[i - 1]:
                    entry.calc_nested_error(error)


    def get_output(self):
        """
        :return: the calculated output of the network
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

for i in range(2000):
    for j in range(len(XORData)):
        perceptron1.set_input(XORData[j][0])
        perceptron2.set_input(XORData[j][0])
        network.update([XORData[j][1]])

for j in range(len(XORData)):
    perceptron1.set_input(XORData[j][0])
    perceptron2.set_input(XORData[j][0])
    print("input: {} activation: {} result: {}".format(XORData[j][0], network.get_output(), XORData[j][1]))
