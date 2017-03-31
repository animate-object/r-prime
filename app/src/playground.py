from app.src.core.cranium import Cranium
from app.src.core.models.lstm_rnn import LstmRnn

from app.src.file.file_utils import song_to_character_sequences
from app.src.file.song_feed import SongFeed
from paths import LYRICS_SETS, DATA_DIR

import os

"""
This class is for testing purposes... plug in any file path to the song_to_sequences function,
mess with the parameters of the LstmRnn (largely copied from the shakespeare example).

You could also plug a different model into the cranium, if you wanted to try something else.
"""

nas_path = os.path.join(LYRICS_SETS, "nas-discography")
output_path = os.path.join(DATA_DIR, "nn-training-output\\")

if not os.path.isdir(output_path):
    os.mkdir(output_path)

feed = SongFeed.from_lyrics_directory(nas_path)


m = LstmRnn(25, feed.character_index, checkpoint_path=output_path)
c = Cranium(model=m)

for i, song in enumerate(feed.get_training_feed(1)):

    print("Processing song {} of {}: {} by {}".format(
        i, len(feed.songs), song.title, song.artist
    ))

    data = {'X': song.X, 'Y': song.Y}
    c.train_model(data, params=dict(epochs=1, batch_size=256))

c.spit(temp=0.5)
