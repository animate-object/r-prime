import inspect


class Cranium:
    must_implement = {'__init__', 'train', 'spit', 'get_state', 'load_state'}

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
        self.model.get_state().save(path)

    def load_state(self, path):
        self.model.load_state(path)

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
