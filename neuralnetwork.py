import numpy as np
import utils

class NeuralNetwork:
    def __init__(self, x, y):
        # 2-layer neural network
        self.n_hidden = 4# 4 neurons in hidden layer
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], self.n_hidden)
        self.weights2 = np.random.rand(self.n_hidden, 2)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def feedforward(self):
        # We might want to use ReLU, Softmax, TanH, Step activation functions instead
        self.layer1 = utils.sigmoid(np.dot(self.input, self.weights1))
        self.output = utils.sigmoid(np.dot(self.layer1, self.weights2))

"""input = []
for i in range(12):
    input.append(100)
x = np.array([input])
nn = NeuralNetwork(x, np.array([[0,0]]))
nn.feedforward()"""
