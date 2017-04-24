from app.src.core.cranium import Cranium
from paths import DATA_DIR
import os.path

saved_model_path = os.path.join(
    DATA_DIR, 'nn-training-output', 'hamburger-rnn-kendrick2'
)

c = Cranium()
c.load_state(saved_model_path)
test_output = c.spit(
    seq_len=2000, temp=0.5, seed="bitch don't kill my vibe ",
    format_filter=True, language_filter=True, english_filter=True, rhyme_filter=True
)
print(test_output)