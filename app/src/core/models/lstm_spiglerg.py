
import tensorflow as tf
import numpy as np
import random
import time
import sys

## RNN with num_layers LSTM layers and a fully-connected output layer
## The network allows for a dynamic number of iterations, depending on the inputs it receives.
##
##    out   (fc layer; out_size)
##     ^
##    lstm
##     ^
##    lstm  (lstm size)
##     ^
##     in   (in_size)

class LstmNnSpiglerg:
    """
    based on code from https://github.com/spiglerg/RNN_Text_Generation_Tensorflow/blob/master/rnn_tf.py
    """

    def __init__(self, in_size, num_layers, out_size, session, learning_rate=0.003, name="rnn"):
        self.scope = name
        self.in_size = in_size
        self.lstm_size = lstm_size
        self.num_layers = num_layers
        self.out_size = out_size
        self.session = session
        self.learning_rate
        pass

    def train(self, step_data):
        pass

    def spit(self, include_metadata=False):
        pass

    def get_state(self):
        pass

    def load_state(self, state):
        pass
