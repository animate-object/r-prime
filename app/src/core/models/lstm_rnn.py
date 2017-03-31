import tflearn
from paths import DATA_DIR
from tflearn import BasicLSTMCell
import tensorflow as tf


class LstmRnn:
    def __init__(self, max_len, char_idx, checkpoint_path=DATA_DIR+'/models-checkpoint/', default_seed=None):
        g = tflearn.input_data([None, max_len, len(char_idx)])
        g = tflearn.lstm(g, 512, return_seq=True)
        g = tflearn.dropout(g, 0.5)
        g = tflearn.lstm(g, 512, return_seq=True)
        g = tflearn.dropout(g, 0.5)
        g = tflearn.lstm(g, 512)
        g = tflearn.dropout(g, 0.5)
        g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
        g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

        self.model = tflearn.SequenceGenerator(
            g, dictionary=char_idx,
            clip_gradients=5.0,
            checkpoint_path=checkpoint_path
        )

        self.default_seed = default_seed if default_seed else "life in the hood"

    def train(self, data, params):
        """
        by default run for one epochs over the training data in batches of 128
        """
        epochs = 1 if not ("epochs" in params) else params["epochs"]
        batch_size = 128 if not ("batch_size" in params) else params["batch_size"]

        X = data["X"]
        Y = data["Y"]
        self.model.fit(
            X, Y,
            validation_set=0.1,
            batch_size=batch_size,
            n_epoch=epochs
        )

    def spit(self, include_meta_data=False, seq_len=200, temp=1.0, seed=None, metaData=None):
        seed = seed if seed else self.default_seed
        output = ""
        if include_meta_data:
            if not metaData:
                raise TypeError("model.spit() called with include_meta_data set to True, but no metadata provided")

        output += self.model.generate(seq_len, temperature=temp, seq_seed=seed)
        return output

    def get_state(self):
        return self.model

    def load_state(self, model):
        self.model = model
