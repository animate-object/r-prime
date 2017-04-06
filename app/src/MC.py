"""
The MC runs the show. It is our application manager class that handles interactions between our back end objects and
the front end.
"""

from app.src.core.cranium import Cranium
from enum import Enum

from app.src.file.song_feed import SongFeed


class AppMode(Enum):
    TRAIN_NEW_MODEL = 1
    LOAD_SAVED_MODEL = 2
    NOT_SET = 3


class MC:
    def __init__(self):
        self.mode = AppMode.NOT_SET
        self.cranium = Cranium()

        # the model to be loaded if loading saved model
        self.saved_model_path = None

        # the location of training data, if training a new model
        self.input_data_path = None

        # the location to write generated text
        self.output_path = None

        # stores the type of model on deck to train. model will be initiated during training phase
        self.model_type = None

        self.training_session = None

    def set_model_type(self, model_type):
        self.model_type = model_type

    def load_model(self, path):
        """
        :param path: path where model checkpoint is stored
        :return:
        """
        try:
            # load the model here
            # . . .
            self.mode = AppMode.LOAD_SAVED_MODEL
            pass
        except FileNotFoundError as e:
            pass
        pass

    def save_model(self):
        pass

    def train_model(self, data_path, epochs, **kwargs):
        feed = SongFeed.from_lyrics_directory(data_path)
        model_init_data = kwargs['model_init_data']
        try:
            m = self.model_type.__init__(feed.character_index, **model_init_data)
        except TypeError as e:
            print("Error creating NN as specified. Missing init params")
            print(e)

        self.cranium.init_model(m)

        self.training_session = SessionMetaData(epochs, len(feed.songs))

        for song in feed.get_training_feed():
            pass


class SessionMetaData:
    """
    Expose some meta data about training sessions to the UI
    """
    def __init__(self, total_epochs, total_song_count):
        self.total_epochs = total_epochs
        self.total_song_count = total_song_count
        self.total_steps = self.total_epochs * self.total_song_count

        self.current_step = 0

    def increment_step_count(self):
        self.current_step += 1

    def percent_completed(self):
        return float(self.total_steps / self.current_step)

