from app.src.core.cranium import Cranium
from app.src.core.models.experimental_rnn_configs import HotDogRnn, JumboDogRnn, HamburgerRnn, PancakeRnn

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

nas_path = os.path.join(LYRICS_SETS, "nas-discography")
sample_path = os.path.join(LYRICS_SETS, "sample-lyric-set")
output_path = os.path.join(DATA_DIR, "nn-training-output\\")
output_path = os.path.join(output_path, "deep_run_3-pancake\\")

if not os.path.isdir(output_path):
    os.mkdir(output_path)

#feed = SongFeed.from_lyrics_directory(sample_path)
feed = SongFeed.from_lyrics_directory(nas_path)

# m = LstmRnn(feed.character_index, seq_max_len=25)
m = PancakeRnn(feed.character_index, seq_max_len=25)
c = Cranium(new_model=m)

epochs = 20


X, Y = feed.get_seq_data()
data = {"X": X, "Y":Y}

for iters in range(epochs):
    c.train_model(data, params={'epochs': 1, 'batch_size': 128})
    if iters%10 == 0:
        c.save_state(output_path)

c.load_state(os.path.join(output_path))

c.spit(seq_len=2000, temp=0.5, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=0.5, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=0.5, seed=feed.seeds[0])
print('='*100)
print('='*100)
c.spit(seq_len=2000, temp=1, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=1, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=1, seed=feed.seeds[0])
print('='*100)
print('='*100)
c.spit(seq_len=2000, temp=0.25, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=0.25, seed=feed.seeds[0])
c.spit(seq_len=2000, temp=0.25, seed=feed.seeds[0])