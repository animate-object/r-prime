import os.path
import pprint

from tflearn.data_utils import string_to_semi_redundant_sequences
from paths import LYRICS_SETS



def song_to_sequences(path):
    """
    Minor modification of the tflearn provided file reader to ignore our artist metadata when processing
    and return the metadata to the caller
    """
    song_text = ""
    metadata = {}
    with open(path, 'r') as song_in:
        for line in song_in:
            if line.startswith("#"):
                continue
            elif line.startswith("["):
                # this is a separate case from the previous. genius uses [] to wrap potentially interesting
                # metadata -- notably verse numbers and contributors. We may want to do something with this
                # information in the future, but it should not go in the sequence data consumed by the models
                continue
            elif line.startswith("~"):
                line_parts = line[1:].split()
                prop_name = line_parts[0]
                prop_val = " ".join(line_parts[1:])
                metadata[prop_name] = prop_val
            else:
                song_text += line

    X, Y, char_idx = string_to_semi_redundant_sequences(song_text)

    return X, Y, char_idx, metadata


# X, Y, char_idx, metadata = song_to_sequences(os.path.join(
#     LYRICS_SETS, "nas-discography", "2nd-childhood.txt"
# ))
#
# # pprint.pprint(metadata)