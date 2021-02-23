import numpy as np
import utils

# A RNN MUST BE IMPLEMENTED. This is a simple feedforward neural network
class NeuralNetwork:
    """
    Output: Vr and Vl values with a range of [0, 1].
    1 means maximum rotation speed in one direction
    0 means maximum rotation speed in the opposite direction
    0.5 means no motion in the corresponding wheel
    """

    def __init__(self, x, y):
        # 2-layer neural network
        self.n_hidden = 4  # 4-neuron hidden layer
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], self.n_hidden)
        self.weights2 = np.random.rand(self.n_hidden, 2)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def feedforward(self):
        # We might want to use ReLU, Softmax, TanH, Step activation functions instead
        self.layer1 = utils.sigmoid(np.dot(self.input, self.weights1))
        self.output = utils.sigmoid(np.dot(self.layer1, self.weights2))

    def update_weights(self):
        # use fitness
        self.weights1 = None
        self.weights2 = None

"""input = []
for i in range(12):
    input.append(100)
x = np.array([input])
nn = NeuralNetwork(x, np.array([[0,0]]))
nn.feedforward()"""
