import numpy as np

class NeuralNetwork:
    def __init__(self, x, y):
        # 2-layer neural network
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1],4)
        self.weights2 = np.random.rand(4,1)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def feedforward(self):
        # We may want to use ReLU, Softmax, TanH, Step activation functions instead
        self.layer1 = np.sigmoid(np.dot(self.input, self.weights1))
        self.output = np.sigmoid(np.dot(self.layer1, self.weights2))
