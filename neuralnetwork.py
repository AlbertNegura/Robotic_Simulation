import numpy as np
import copy
import utils
import config

class RNN:
    """
    Output: Vl and Vr values with a range of [0, 1].
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


        # TODO: I thought we were just going to use 1 hidden layer, this implies at least 2
        self.synapse_h = 2*np.random.random((hidden_dim, hidden_dim)) - 1

        # initialize previous step layer values
        self.layer_1_values = list()
        self.layer_1_values.append(np.zeros(hidden_dim))

    def feedforward(self, x):
        """
        :param x: robot.sensor_values()
        :return: Vr,Vl
        """
        # hidden layer (input ~+ prev_hidden)
        # self.layer_1 = utils.sigmoid(np.dot(self.input, self.synapse_0) + np.dot(self.layer_1_values[-1], self.synapse_h))
        self.layer_1 = utils.sigmoid(np.dot(self.input, self.synapse_0))

        # output layer
        self.output = utils.sigmoid(np.dot(self.layer_1, self.synapse_1))

        # store hidden layer so we can use it in the next time step
        self.layer_1_values.append(copy.deepcopy(self.layer_1))
        return self.round_output(self.output)

    def update_weights(self):
        # use fitness
        self.synapse_0 = None
        self.synapse_1 = None
        self.synapse_h = None

    def round_output(self):
        """
        self.output is a length 2 vector with values in a [0, 1] range.
        We need this values to be strictly 0, 1 or 0.5.
        """
        r_list = [0, 0.5, 1]
        round_values = []
        for i in range(self.output_dim):
            round_values.append(min(r_list, key=lambda x:abs(x-self.output[0,i])))
        return round_values

    def weight_vector(self):
        weights = np.concatenate((self.synapse_0, self.synapse_1.transpose()), axis=0).flatten()
        return weights

"""input = []
for i in range(12):
    input.append(100)
x = np.array([input])
nn = RNN(x, np.array([[0,0]]))
nn.feedforward(x)
nn.feedforward(x)"""
