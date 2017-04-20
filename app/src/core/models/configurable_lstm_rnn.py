import tflearn


class ConfigurableLstmRnn:
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None, default_seed=None, **kwargs):

        g = self._build_model(seq_max_len, len(char_idx), **kwargs)

        self.model = tflearn.SequenceGenerator(
            g, dictionary=char_idx,
            clip_gradients=5.0,
            checkpoint_path=checkpoint_path
        )

        self.default_seed = default_seed if default_seed else "life in the hood"

    def _build_model(self, seq_max_len, len_char_idx, **kwargs):
        hidden_layer_sizes = kwargs['hidden_layer_sizes'] if 'hidden_layer_sizes' in kwargs else [512, 512]
        optimization_algorithm = kwargs['optimization_algorithm'] if  'optimization_algorithm' in kwargs else 'adam'
        loss_function = kwargs['loss_function'] if 'loss_function' in kwargs else 'categorical_crossentropy'
        learning_rate = kwargs['learning_rate'] if 'learning_rate' in kwargs else 0.001
        activation_function = kwargs['activation_function'] if 'activation_function' in kwargs else 'softmax'
        final_layer_size = kwargs['final_layer_size'] if 'final_layer_size' in kwargs else 512

        g = tflearn.input_data([None, seq_max_len, len_char_idx])
        for i in range(len(hidden_layer_sizes)):
            g = tflearn.lstm(g, hidden_layer_sizes[i], return_seq=True)
        g = tflearn.lstm(g, final_layer_size)
        g = tflearn.dropout(g, 0.5)
        g = tflearn.fully_connected(g, len_char_idx, activation=activation_function)
        g = tflearn.regression(
            g,
            optimizer=optimization_algorithm,
            loss=loss_function,
            learning_rate=learning_rate
        )

        return g

    def train(self, data, params=dict()):
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

    def load_state(self, path):
        self.model.load(path)
