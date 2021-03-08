"""
Robotic Simulation Software RNN class
Authors:
Albert Negura
Sergi Nogues Farres
"""
from config import *
import numpy as np
import copy
import utils

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
        self.synapse_h = 2*np.random.random((hidden_dim, hidden_dim)) - 1

        # initialize previous step layer values
        self.layer_1_values = list()
        self.layer_1_values.append(np.zeros(hidden_dim))

    def feedforward(self, x):
        """
        :param x: robot.sensor_values()
        :return: Vr,Vl
        """
        self.input = x[0]

        # hidden layer (input ~+ prev_hidden)
        self.input = np.round(self.input, 5)
        prev_values = np.round(self.layer_1_values[-1], 5)
        self.layer_1 = utils.sigmoid(np.dot(self.input, self.synapse_0) + np.dot(prev_values, self.synapse_h)) if RNN else utils.sigmoid(np.dot(self.input, self.synapse_0))

        # output layer
        np.round(self.layer_1, 5)
        self.output = utils.tanh(np.dot(self.layer_1, self.synapse_1))

        # store hidden layer so we can use it in the next time step
        self.layer_1_values.append(copy.deepcopy(self.layer_1))
        return np.round(self.output,5)

    def update_weights(self, weights_list):
        """
        synapse_0 = 12*4
        synapse_h = 4*4
        synapse_1 = 4*2
        """
        # nn weights
        synapse_0 = 2*np.random.random((self.input_dim, self.hidden_dim)) - 1
        synapse_1 = 2*np.random.random((self.hidden_dim, self.output_dim)) - 1
        synapse_h = 2*np.random.random((self.hidden_dim, self.hidden_dim)) - 1

        pos = 0
        if type(weights_list) == list:
            for row in range(self.input_dim):
                for col in range(self.hidden_dim):
                    synapse_0[row, col] = weights_list[pos]
                    pos = pos+1
            for row in range(self.hidden_dim):
                for col in range(self.hidden_dim):
                    synapse_h[row, col] = weights_list[pos]
                    pos = pos+1
            for col in range(2):
                for row in range(self.hidden_dim):
                    synapse_1[row, col] = weights_list[pos]
                    pos = pos+1
        else:
            for row in range(self.input_dim):
                for col in range(self.hidden_dim):
                    synapse_0[row, col] = weights_list.genome[pos]
                    pos = pos+1
            for row in range(self.hidden_dim):
                for col in range(self.hidden_dim):
                    synapse_h[row, col] = weights_list.genome[pos]
                    pos = pos+1
            for col in range(2):
                for row in range(self.hidden_dim):
                    synapse_1[row, col] = weights_list.genome[pos]
                    pos = pos+1

        self.synapse_h = synapse_h
        self.synapse_0 = synapse_0
        self.synapse_1 = synapse_1

        # initialize previous step layer values
        self.layer_1_values = list()
        self.layer_1_values.append(np.zeros(self.hidden_dim))


    def round_output(self):
        """
        return values to be strictly 0, 1 or 0.5.
        """
        r_list = [0, 0.5, 1]
        round_values = []
        for i in range(self.output_dim):
            round_values.append(min(r_list, key=lambda x:abs(x-self.output[i])))
        return round_values

    def weight_vector(self):
        weights = np.concatenate((self.synapse_0, self.synapse_h, self.synapse_1.transpose()), axis=0).flatten()
        return weights

"""input = []
for i in range(12):
    input.append(100)
x = np.array([input])
nn = RNN(x, np.array([[0,0]]))
nn.feedforward(x)
nn.feedforward(x)"""
