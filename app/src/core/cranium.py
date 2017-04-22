import inspect

from app.src.core.models.configurable_lstm_rnn import ConfigurableLstmRnn
from app.src.domain.default_char_index import create_char_index
import pickle
import os.path


class Cranium:
    must_implement = {'__init__', 'train', 'spit', 'get_state', 'load_state', 'get_init_params'}

    def __init__(self, new_model=None):
        self.model = None
        if new_model:
            self.init_model(new_model)

    def init_model(self, model):
        self._verify(model)
        self.model = model

    def train_model(self, data, params=None):
        if params:
            return self.model.train(data, params)
        return self.model.train(data)

    def spit(self, include_metadata=False, filter_functions=[], **kwargs):
        raw_output = self.model.spit(include_metadata, **kwargs)
        text = raw_output
        for filter_function in filter_functions:
            text = filter_function(text)
        return text

    def save_state(self, path):
        params = self.model.get_init_params()
        self._save_model_init_params(path, params)
        model_checkpoint = os.path.join(path, 'model.checkpoint')
        self.model.get_state().save(model_checkpoint)

    def load_state(self, path):
        params = self._load_model_init_params(path)
        self.model = ConfigurableLstmRnn(create_char_index(), seq_max_len=25, checkpoint_path=None, **params)
        model_checkpoint = os.path.join(path, 'model.checkpoint')
        self.model.load_state(model_checkpoint)

    def _verify(self, model):
        method_tups = inspect.getmembers(model, inspect.ismethod)
        implemented = set([tup[1].__name__ for tup in method_tups])
        not_implemented = self.must_implement - implemented

        if not_implemented:
            missing_methods = ', '.join(not_implemented)
            # this should probably be a TypeError
            raise TypeError(
                "Submitted model of type {} does not implement required method(s): {}.".format(
                    type(model), missing_methods
                )
            )

    def _save_model_init_params(self, path, params):
        model_config_path = os.path.join(path, 'model.config')
        pickle.dump(params, open(model_config_path, 'wb'))

    def _load_model_init_params(self, path):
        model_config_path = os.path.join(path, 'model.config')
        return pickle.load(open(model_config_path, 'rb'))

# ------------------------------------------------------------------
# MANUAL TEST FUNCTIONS
# ------------------------------------------------------------------
#
#
# class TestVerifyNN:
#     def __init__(self):
#         pass
#
#     def train(self, step_data):
#         pass
#
#     def spit(self, include_metadata=False):
#         pass
#
#     def get_state(self, state):
#         pass
#
#     def load_state(self, state):
#         pass
#
#
# if __name__ == '__main__':
#     t = TestVerifyNN()
#     c = Cranium(t)
