import numpy as np
import copy
import utils

class RNN:
    """
    Output: Vr and Vl values with a range of [0, 1].
    1 means maximum rotation speed in one direction
    0 means maximum rotation speed in the opposite direction
    0.5 means no motion in the corresponding wheel
    """

    def __init__(self, x, y, input_dim=12, hidden_dim=4, output_dim=2):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.input = x
        self.y = y
        self.output = np.zeros(self.y.shape)

        # nn weights
        self.synapse_0 = 2*np.random.random((input_dim, hidden_dim)) - 1
        self.synapse_1 = 2*np.random.random((hidden_dim, output_dim)) - 1
        self.synapse_h = 2*np.random.random((hidden_dim, hidden_dim)) - 1

        # initialize previous step layer values
        self.layer_1_values = list()
        self.layer_1_values.append(np.zeros(hidden_dim))

    def feedforward(self):
        # hidden layer (input ~+ prev_hidden)
        self.layer_1 = utils.sigmoid(np.dot(self.input, self.synapse_0) + np.dot(self.layer_1_values[-1], self.synapse_h))

        # output layer
        self.output = utils.sigmoid(np.dot(self.layer_1, self.synapse_1))

        # store hidden layer so we can use it in the next time step
        self.layer_1_values.append(copy.deepcopy(self.layer_1))

    def update_weights(self):
        # use fitness
        self.synapse_0 = None
        self.synapse_1 = None
        self.synapse_h = None

"""input = []
for i in range(12):
    input.append(100)
x = np.array([input])
nn = RNN(x, np.array([[0,0]]))
nn.feedforward()"""
