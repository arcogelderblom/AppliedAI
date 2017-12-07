import random
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def derivativeSigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

class Perceptron:
    bias = -1

    def __init__(self, inputs, learnRate=0.1):
        # Add a bias
        self.input = inputs + [self.bias]
        self.weights = []

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

"""
    NIET MET EEN ADDER DOEN
    DEZE OPDRACHT UIVOEREN MET EEN XOR
"""

#######
# OR #
#######
trainingOR =  [ [[0,0], 0],
                [[0,1], 1],
                [[1,0], 1],
                [[1,1], 1]]

OR = Perceptron(trainingOR[0][0])
for j in range(100):
    for i in range(len(trainingOR)):
        OR.set_input(trainingOR[i][0])
        OR.update(trainingOR[i][1])
print("OR RESULT")
for i in range(len(trainingOR)):
    OR.set_input(trainingOR[i][0])
    OR.update(trainingOR[i][1])
    print("{:2} {:20} {}".format(trainingOR[i][1], OR.get_activation(), 1 if OR.get_activation() > 0.6 else 0))

########
# NAND #
########
trainingNAND = [[[0,0], 1],
                [[0,1], 1],
                [[1,0], 1],
                [[1,1], 0]]

NAND = Perceptron(trainingNAND[0][0])
for k in range(200):
    for i in range(len(trainingNAND)):
        NAND.set_input(trainingNAND[i][0])
        NAND.update(trainingNAND[i][1])
print("NAND RESULT")
for i in range(len(trainingNAND)):
    NAND.set_input(trainingNAND[i][0])
    NAND.update(trainingNAND[i][1])
    print("{:2} {:20} {}".format(trainingNAND[i][1], NAND.get_activation(), 1 if NAND.get_activation() > 0.55 else 0))

########
# AND #
########
trainingAND = [ [[0,0], 0],
                [[0,1], 0],
                [[1,0], 0],
                [[1,1], 1]]

AND = Perceptron(trainingAND[0][0])
for l in range(100):
    for i in range(len(trainingAND)):
        AND.set_input(trainingAND[i][0])
        AND.update(trainingAND[i][1])
print("AND RESULT")
for i in range(len(trainingAND)):
    AND.set_input(trainingAND[i][0])
    AND.update(trainingAND[i][1])
    print("{:2} {:20} {}".format(trainingAND[i][1], AND.get_activation(), 1 if AND.get_activation() > 0.45 else 0))
