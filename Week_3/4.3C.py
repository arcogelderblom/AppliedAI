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

"""
    NIET MET EEN ADDER DOEN
    DEZE OPDRACHT UIVOEREN MET EEN XOR
"""

########
# XOR #
########
trainingXOR =  [[[0,0], 0],
                [[0,1], 1],
                [[1,0], 1],
                [[1,1], 0]]

XOR = Perceptron(trainingXOR[0][0])
for j in range(800):
    for i in range(len(trainingXOR)):
        XOR.set_input(trainingXOR[i][0])
        XOR.update(trainingXOR[i][1])
print("XOR RESULT")
for i in range(len(trainingXOR)):
    XOR.set_input(trainingXOR[i][0])
    XOR.update(trainingXOR[i][1])
    print("{:2} {:20} {}".format(trainingXOR[i][1], XOR.get_activation(), 1 if XOR.get_activation() > 0.5 else 0))

########
# NAND #
########
trainingNAND = [[[0,0], 1],
                [[0,1], 1],
                [[1,0], 1],
                [[1,1], 0]]

NAND = Perceptron(trainingNAND[0][0])
for j in range(150):
    for i in range(len(trainingNAND)):
        NAND.set_input(trainingNAND[i][0])
        NAND.update(trainingNAND[i][1])
print("NAND RESULT")
for i in range(len(trainingNAND)):
    NAND.set_input(trainingNAND[i][0])
    NAND.update(trainingNAND[i][1])
    print("{:2} {:20} {}".format(trainingNAND[i][1], NAND.get_activation(), 1 if NAND.get_activation() > 0.5 else 0))

"""
#########
# ADDER #
#########
trainingADDER = [[[0,0], [0,0]],
                 [[1,0], [1,0]],
                 [[0,1], [1,0]],
                 [[1,1], [0,1]]]
ADDER1 = Perceptron(trainingADDER[0][0])
ADDER2 = Perceptron([trainingADDER[0][0][0], ADDER1.get_activation()])
ADDER3 = Perceptron([ADDER1.get_activation(), trainingADDER[0][1][0]])
ADDER4 = Perceptron([ADDER2.get_activation(), ADDER3.get_activation()])
ADDER5 = Perceptron([ADDER1.get_activation(), ADDER1.get_activation()])

for j in range(10000):
    for i in range(len(trainingADDER)):
        ADDER1.set_input(trainingADDER[i][0])
        ADDER2.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
        ADDER3.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
        ADDER4.update(trainingADDER[i][1][0])
        ADDER5.update(trainingADDER[i][1][1])

print("ADDER RESULT")
print("ADDER4 'X (+) Y'")
for i in range(len(trainingADDER)):
    ADDER1.set_input(trainingADDER[i][0])
    ADDER2.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
    ADDER3.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
    ADDER4.update(trainingADDER[i][1][0])
    ADDER5.update(trainingADDER[i][1][1])
    print(trainingADDER[i][1][0], ADDER4.get_activation())
print("ADDER5 'X * Y'")
for i in range(len(trainingADDER)):
    ADDER1.set_input(trainingADDER[i][0])
    ADDER2.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
    ADDER3.set_input([trainingADDER[i][0][0], ADDER1.get_activation()])
    ADDER4.update(trainingADDER[i][1][0])
    ADDER5.update(trainingADDER[i][1][1])
    print(trainingADDER[i][1][1], ADDER5.get_activation())
"""