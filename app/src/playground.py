from app.src.core.cranium import Cranium
from app.src.core.models.lstm_rnn import LstmRnn

from app.src.file.file_utils import read_song
from app.src.file.song_feed import SongFeed
from paths import LYRICS_SETS, DATA_DIR

import os

"""
This class is for testing purposes... plug in any file path to the song_to_sequences function,
mess with the parameters of the LstmRnn (largely copied from the shakespeare example).

You could also plug a different model into the cranium, if you wanted to try something else.
"""

nas_path = os.path.join(LYRICS_SETS, "nas-discography")
sample_path = os.path.join(LYRICS_SETS, "sample-lyric-set")
output_path = os.path.join(DATA_DIR, "nn-training-output\\")
l_a_b = os.path.join(sample_path, "life's-a-bitch.txt")

if not os.path.isdir(output_path):
    os.mkdir(output_path)

# feed = SongFeed.from_lyrics_directory(sample_path)
feed = SongFeed.from_lyrics_files(l_a_b)

m = LstmRnn(feed.character_index, seq_max_len=25)
c = Cranium(new_model=m)

epochs = 10


X, Y = feed.get_seq_data()
data = {"X": X, "Y":Y}
c.train_model(data, params={'epochs': epochs, 'batch_size': 128})

c.spit(seq_len=2000, temp=0.5)
