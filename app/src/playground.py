from app.src.core.cranium import Cranium
from app.src.core.models.experimental_rnn_configs import *
from app.src.file.song_feed import SongFeed
from paths import LYRICS_SETS, DATA_DIR
import tensorflow as tf
import os

"""
This class is for testing purposes... plug in any file path to the song_to_sequences function,
mess with the parameters of the LstmRnn (largely copied from the shakespeare example).

You could also plug a different model into the cranium, if you wanted to try something else.
"""

tf.reset_default_graph()

input_path = os.path.join(LYRICS_SETS, "beastie-boys")
output_path = os.path.join(DATA_DIR, "nn-training-output\\")
output_path = os.path.join(output_path, "beastie-boys-wide-rnn-1\\")

if not os.path.isdir(output_path):
    os.mkdir(output_path)

feed = SongFeed.from_lyrics_directory(input_path, strip_newlines=True)

m = HamburgerRnn(feed.character_index, seq_max_len=25)
c = Cranium(new_model=m)

epochs = 15

X, Y = feed.get_seq_data()
data = {"X": X, "Y": Y}

c.model.init_params['default_seed'] = feed.seeds[0]

c.train_model(data, params={'epochs': epochs, 'batch_size': 128})



c.save_state(output_path)
print('='*100)
print(c.spit(seq_len=2000, temp=0.5, seed=feed.seeds[0]))
print('='*100)
print(c.spit(seq_len=2000, temp=1, seed=feed.seeds[0]))
print('='*100)
print(c.spit(seq_len=2000, temp=0.25, seed=feed.seeds[0]))