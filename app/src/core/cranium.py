import inspect


class Cranium:
    must_implement = {'__init__', 'train', 'spit', 'get_state', 'load_state'}

    def __init__(self, model):
        self._verify(model)
        self.model = model

    def train_model(self, step_data):
        return self.model.train(step_data)

    def spit(self, include_metadata=False, **kwargs):
        to_file, path = kwargs.get('to_file'), kwargs.get('file_path')
        if to_file:
            if not path:
                raise TypeError("Cannot write to file. Specify output locale as 'file_path'")
            else:
                output = self.model.spit(include_metadata)
                pass  # raise missing parameter exception on missing path param

        else:
            print(self.model.spit(include_metadata))
            pass  # write nn output to console

    def save_state(self, path):
        state = self.model.get_state()
        pass  # save state to path

    def load_state(self, path):
        state = None  # retrieve this from file at path
        self.model.load_state(state)

    def _verify(self, model):
        method_tups = inspect.getmembers(model, inspect.ismethod)
        implemented = set([tup[1].__name__ for tup in method_tups])
        not_implemented = self.must_implement - implemented

        if not_implemented:
            missing_methods = ', '.join(not_implemented)
            raise NotImplementedError(
                "Submitted model of type {} does not implement required method(s): {}.".format(
                    type(model), missing_methods
                )
            )

# ------------------------------------------------------------------
# MANUAL TEST FUNCTIONS
# ------------------------------------------------------------------


class TestVerifyNN:
    def __init__(self):
        pass

    def train(self, step_data):
        pass

    def spit(self, include_metadata=False):
        pass

    def get_state(self, state):
        pass

    def load_state(self, state):
        pass


if __name__ == '__main__':
    t = TestVerifyNN()
    c = Cranium(t)
