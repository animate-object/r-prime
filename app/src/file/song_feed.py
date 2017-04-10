"""
The purpose of this class is to build and manage a collection of songs and metadata to provide to the models, and
provide some kind of generator type functionality with a concept of the *next* song in the data.

The structure wraps a *tuple* of songs. The tuple functions as an immutable list. The logic behind this is that to
train our NNs we may want to loop over a collection of songs and ensure that each song is factored equally into the
training data. In any event we want to explicitly preserve order so we can provide a generator function that loops
repeatedly over the training data in a predictable manner.
"""

import os.path
import random
import math

from tflearn.data_utils import string_to_semi_redundant_sequences, random_sequence_from_string

from app.src.domain.default_char_index import create_char_index
from app.src.file.file_utils import read_song
from app.src.domain.song import Song

import string


class SongFeed:
    def __init__(self, sequence_function=read_song):
        self.file_parser_function = sequence_function
        self.songs = set()
        self.artists = set()

        self.X = None
        self.Y = None

        self.cumulative_character_count = 0

        # the cumulative character index of all songs in the data set
        self.character_index = create_char_index()
        self.seeds = []

    @classmethod
    def from_lyrics_directory(cls, directory_path):
        """
        Build the song feed from a directory containing raw lyrics text files.
        :param path:
        :return: a SongFeed
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(
                "Cannot create song feed from directory. Directory not found at provided path:\n\t{}"
                .format(directory_path)
            )

        paths = [entry.path for entry in os.scandir(directory_path)]
        if not paths:
            raise FileNotFoundError(
                "Cannot create song feed. Provided directory was empty:\n\t{}"
                .format(directory_path)
            )

        return cls.from_lyrics_files(*paths)

    @classmethod
    def from_lyrics_files(cls, *paths, num_seeds=10):
        """
        Read in songs individually from a collection of paths
        :param paths: paths where song data is located
        :return: a SongFeed
        """
        feed = SongFeed()
        collected_songs = []
        for path in paths:
            try:
                text, meta_data = feed.file_parser_function(path)

                # Checking for song meta data... there must be a better way
                artist = meta_data.pop('ARTIST') if 'ARTIST' in meta_data else None
                title = meta_data.pop('TITLE') if 'TITLE' in meta_data else None
                collaborators = meta_data.pop('COLLABORATORS') if 'COLLABORATORS' in meta_data else None
                year = meta_data.pop('YEAR') if 'YEAR' in meta_data else None

                collected_songs.append(
                    Song(
                        text=text,
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
        complete_text = ""

        for song in feed.songs:
            complete_text += song.text

        feed._build_sequence_data_from_songs(complete_text)
        feed._get_seeds(num_seeds, text=complete_text)

        return feed

    def _build_sequence_data_from_songs(self, text):
        self.X, self.Y, _ = string_to_semi_redundant_sequences(text, 25, char_idx=self.character_index) #FIXME make max len configurable

    def _get_seeds(self, n, text):
        for _ in range(n):
            self.seeds.append(random_sequence_from_string(text, 25)) #FIXME make max len configurable

    def get_seq_data(self):
        return self.X, self.Y
