input vector = 567
activation HL1 = 64
activation HL2 = 16
activation HL3 = 16
ouput vector = 4

Dimensies:
inputVector = 567 * 1
oHL1 = 64 * 567
oHL2 = 16 * 64
oHL3 = 16 * 16
ouputVector = 4 * 16
biasHL1 = 64 * 1
biasHL2 = 16 * 1
biasHL3 = 16 * 1
biasOutput = 4 * 1

aHL1 = sigmoid(oHL1 * inputVector + biasHL1)
aHL2 = sigmoid(oHL2 * aHL1 + biasHL2)
aHL3 = sigmoid(oHL3 * aHL2 + biasHL3)
y = sigmoid(ouputVector * aHL3 + biasOutput)
oftewel:
y = sigmoid(ouputVector * sigmoid(oHL3 * sigmoid(oHL2 * sigmoid(oHL1 * inputVector + biasHL1) + biasHL2) + biasHL3) + biasOutput)
