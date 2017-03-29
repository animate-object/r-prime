"""
The purpose of this class is to build and manage a collection of songs and metadata to provide to the models, and
provide some kind of generator type functionality with a concept of the *next* song in the data.

The structure wraps a *tuple* of songs. The tuple functions as an immutable list. The logic behind this is that to
train our NNs we may want to loop over a collection of songs and ensure that each song is factored equally into the
training data. In any event we want to explicitly preserve order so we can provide a generator function that loops
repeatedly over the training data in a predictable manner.
"""

import os.path
from pprint import pprint

from app.src.file.file_utils import song_to_character_sequences
from app.src.domain.song import Song
from paths import LYRICS_SETS

import string

class SongFeed:
    def __init__(self, sequence_function=song_to_character_sequences):
        self.file_parser_function = sequence_function
        self.songs = None
        self.artists = set()

        # the cumulative character index of all songs in the data set
        self.character_index = None

    @classmethod
    def from_lyrics_directory(cls, directory_path):
        """
        Build the song feed from a directory containing raw lyrics text files.
        :param path:
        :return: a SongFeed
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError("Directory not found at provided path:\n\t{}".format(directory_path))
        paths = [entry.path for entry in os.scandir(directory_path)]
        if not paths:
            raise FileNotFoundError("Provided directory was empty:\n\t{}".format(directory_path))
        return cls.from_lyrics_files(*paths)

    @classmethod
    def from_lyrics_files(cls, *paths):
        """
        Read in songs individually from a collection of paths
        :param paths: paths where song data is located
        :return: a SongFeed
        """
        feed = SongFeed()
        collected_songs = []
        idx = create_char_index()
        for path in paths:
            try:
                X, Y, _, meta_data = feed.file_parser_function(path, provided_char_index=idx)

                # Checking for song meta data... there must be a better way
                artist = meta_data.pop('ARTIST') if 'ARTIST' in meta_data else None
                title = meta_data.pop('TITLE') if 'TITLE' in meta_data else None
                collaborators = meta_data.pop('COLLABORATORS') if 'COLLABORATORS' in meta_data else None
                year = meta_data.pop('YEAR') if 'YEAR' in meta_data else None

                collected_songs.append(
                    Song(
                        X, Y,
                        artist=artist,
                        title=title,
                        collaborators=collaborators,
                        year=year,
                        **meta_data if meta_data else {}  # if there's any non standard meta data, store it on the song
                    )
                )
                if artist:
                    feed.artists.add(artist)
            except FileNotFoundError as e:
                # We don't want to error out for one bad file
                # FIXME log instead of print
                print("Skipped missing file")

        feed.songs = tuple(sorted(collected_songs, key=lambda x: x.title))
        feed.character_index = idx
        return feed

    def get_training_feed(self, iterations=1):
        assert type(iterations) == int
        while iterations > 0:
            for song in self.songs:
                yield song
            iterations -= 1


def create_char_index():
    return {char: i for (i, char) in enumerate(string.printable)}

# # --- manual tests ---
# sample_path = os.path.join(LYRICS_SETS, "sample-lyric-set")
# test_feed = SongFeed.from_lyrics_directory(sample_path)
#
# print()
