class Perceptron:
    input = [[]]
    bias = 0

    def __init__(self, input, bias=0):
        self.input = input
        self.bias = bias

    """
    Get the activation of the neuron. Returns 1 if the calculated sum + bias is higher than
    the 0, otherwise output is 0
    """
    def getActivation(self):
        return 1 if sum(x[0]*x[1] for x in self.input) + self.bias > 0 else 0

NORinput1 = [0, -1/3]
NORinput2 = [0, -1/3]
NORinput3 = [0, -1/3]
NOR = Perceptron([NORinput1, NORinput2, NORinput3], 1/3)
print(NOR.getActivation())

ADDERinput1 = [0, -0.5]
ADDERinput2 = [0, -0.5]
NAND1 = Perceptron([ADDERinput1, ADDERinput2], 1)
NAND2 = Perceptron([ADDERinput1, [NAND1.getActivation(), -0.5]], 1)
NAND3 = Perceptron([[NAND1.getActivation(), -0.5], ADDERinput2], 1)
NAND4 = Perceptron([[NAND2.getActivation(), -0.5], [NAND3.getActivation(), -0.5]], 1)
NAND5 = Perceptron([[NAND1.getActivation(), -0.5], [NAND1.getActivation(), -0.5]], 1)
print("X1 (+) X2: {}".format(NAND4.getActivation()))
print("X1 * X2: {}".format(NAND5.getActivation()))
