from app.src.core.models.configurable_lstm_rnn import ConfigurableLstmRnn

class OriginalRnn(ConfigurableLstmRnn):
    """
    The baseline RNN we based the others on - 3 layers of 512 neurons
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(
            char_idx, seq_max_len, checkpoint_path, hidden_layer_sizes=[512, 512], final_layer_size=512
        )

class HotDogRnn(ConfigurableLstmRnn):
    """
    This class defines a deep but narrow LstmRnn.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path, hidden_layer_sizes=[256, 256, 256, 256, 256, 256])


class JumboDogRnn(ConfigurableLstmRnn):
    """
    This class defines a deep, wide LstmRnn.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path, hidden_layer_sizes=[512, 512, 512, 512, 512, 512])



class HamburgerRnn(ConfigurableLstmRnn):
    """
    Wide, shallow network.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path,
                         hidden_layer_sizes=[1024], final_layer_size=1024)


class PancakeRnn(ConfigurableLstmRnn):
    """
    Wide, very shallow network.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path, hidden_layer_sizes=[1024])



class PizzaDoughRnn(ConfigurableLstmRnn):
    """
    Very wide, very shallow network.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path,
                        hidden_layer_sizes=[],
                        final_layer_size=2048)



class LittleRnn(ConfigurableLstmRnn):
    """
    Very tiny rnn. Trains quickly for testing.
    """
    def __init__(self, char_idx, seq_max_len=25, checkpoint_path=None):
        super().__init__(char_idx, seq_max_len, checkpoint_path,
                         hidden_layer_sizes=[],
                         final_layer_size=64)

