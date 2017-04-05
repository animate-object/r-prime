from tflearn.data_utils import string_to_semi_redundant_sequences
from string import punctuation
from re import sub as regex_sub
# TODO make configurable. Copied code lives in song_feed char index method


def read_song(path):
    """
    Get metadata from song file, and remove unicode and non printables from the song text.
    :return: the song test and a map of song metadata
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
                song_text += _remove_unicode(line)

    return song_text, metadata


def _remove_unicode(string):
    return regex_sub(r'[^\x00-\x7F]+', '', string)

# X, Y, char_idx, metadata = song_to_sequences(os.path.join(
#     LYRICS_SETS, "nas-discography", "2nd-childhood.txt"
# ))
#
# # pprint.pprint(metadata)
