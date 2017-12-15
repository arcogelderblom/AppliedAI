import numpy as np

xTotal = np.matrix([[1],[1],[1]])
oTotal = np.matrix([[0.1, -0.2, -0.3],
                   [0.4, -0.5, -0.6],
                   [-0.7, -0.8, -0.9],
                   [0.1, 0.2, 0.3]])

xSeperated = np.matrix([[1],[1]])
oSeperated = np.matrix([[-0.2, -0.3],
                       [-0.5, -0.6],
                       [-0.8, -0.9],
                       [0.2, 0.3]])
b = np.matrix([[0.1], [0.4], [-0.7], [0.1]])

if (oTotal*xTotal).all() == (oTotal*xTotal).all():
    print("These are the same.")
    print(oTotal*xTotal)
    print((oSeperated*xSeperated)+b)