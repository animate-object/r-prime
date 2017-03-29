from app.src.core.cranium import Cranium
from app.src.core.models.lstm_rnn import LstmRnn

from app.src.file.file_utils import song_to_sequences
from paths import LYRICS_SETS, DATA_DIR

import os

"""
This class is for testing purposes... plug in any file path to the song_to_sequences function,
mess with the parameters of the LstmRnn (largely copied from the shakespeare example).

You could also plug a different model into the cranium, if you wanted to try something else.
"""

path = os.path.join(LYRICS_SETS, "nas-discography", "life's-a-bitch.txt")
output_path = os.path.join(DATA_DIR, "nn-training-output\\")

if not os.path.isdir(output_path):
    os.mkdir(output_path)

X, Y, chr_idx, metadata = song_to_sequences(path)
data = {'X': X, 'Y': Y}


m = LstmRnn(25, chr_idx, checkpoint_path=output_path)
c = Cranium(model=m)

c.train_model(data, params=dict(epochs=2, batch_size=256))

c.spit()
