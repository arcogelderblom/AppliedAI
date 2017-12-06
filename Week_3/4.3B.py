import random
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def derivativeSigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

class Perceptron:
    weights = []
    input = []
    learnRate = 0
    bias = -1

    def __init__(self, inputs, learnRate=0.1):
        # Add a bias
        self.input = inputs + [self.bias]

        for entry in self.input:
            self.weights.append(random.random())
        self.learnRate = learnRate

    def get_sum(self):
        sum = 0
        for i in range(len(self.input)):
            sum += self.input[i] * self.weights[i]
        return sum


    def update(self, expected):
        differences = []

        for entry in self.input:
            tmp = self.learnRate * entry * derivativeSigmoid(self.get_sum()) * (expected - self.get_activation())
            differences.append(tmp)

        for i in range(len(differences)):
            self.weights[i] = self.weights[i] + differences[i]

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
        return sigmoid(self.get_sum())

    def __repr__(self):
        tmp = ""
        for i in range(len(self.input)):
            tmp += "Input: " + str(self.input[i]) + " Weight: " + str(self.weights[i]) + "\n"
        tmp += "Current output with these settings: " + str(self.get_activation()) + "\n"
        return tmp

#######
# NOR #
#######          1|2|3|  output
trainingNOR = [[[0,0,0], 1],
               [[1,0,0], 0],
               [[1,1,0], 0],
               [[1,1,1], 0],
               [[0,1,0], 0],
               [[0,1,1], 0],
               [[0,0,1], 0],
               [[1,0,1], 0]]

NOR = Perceptron(trainingNOR[0][0])
for j in range(100):
    for i in range(len(trainingNOR)):
        NOR.set_input(trainingNOR[i][0])
        NOR.update(trainingNOR[i][1])

print("NOR RESULTS:")
for i in range(len(trainingNOR)):
    NOR.set_input(trainingNOR[i][0])
    print("{:2} {:20} {}".format(trainingNOR[i][1], NOR.get_activation(), 1 if NOR.get_activation() > 0.19 else 0))
