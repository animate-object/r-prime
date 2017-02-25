from app.src.domain.song import Song
from paths import DATA_DIR
import os.path


class SongReader:
    """
    Handles file input around reading in lyric sets and while parsing/sanitizing data, compiles initial
    """
    def __init__(self, path=""):
        self.term_dictionary = {"<!PLACEHOLDER>": 0}
        self.reverse_term_dict = {0: "<!PLACEHOLDER>"}
        self.dict_size = 0  # allows us to avoid calling max (O(n))
        self.songs = []
        # table to remove line punctuation with str.translate
        self.line_sanitizer_table = str.maketrans("", "", "{}*:!.,<>&(),?&;\"")
        self.word_sanitizer_table = str.maketrans("", "", "-")

    def read_file(self, path_to_song):
        with open(path_to_song, "r", encoding="utf-8") as fileIn:
            song_text, artist, title = "", None, None
            for line in fileIn:
                # we may want to other things in these cases in the future.
                if line.startswith("#"):
                    continue
                elif line.startswith("["):
                    continue  # TODO add to collaborators?
                elif line.startswith("~"):
                    if line.startswith("~ARTIST"):
                        artist = line.split()[1]
                    elif line.startswith("~TITLE"):
                        title = " ".join(line.split()[1:])
                else:
                    song_text += self._parse_line(line)
            self.songs.append(Song(text=song_text, artist=artist, title=title))

    def batch_read_files(self, path_to_folder):
        all_contents = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder)]
        text_file_paths = [f for f in all_contents if os.path.isfile(f) and f.endswith(".txt")]

        for file_path in text_file_paths:
            self.read_file(file_path)

    def _parse_line(self, line):
        line = line.translate(self.line_sanitizer_table)
        for word in line.split():
            word = self._sanitize_word(word)
            if word and word not in self.term_dictionary:
                self._add_word_to_dicts(word)
        return line

    def _add_word_to_dicts(self, word):
        # is this computationally prohibitive?
        val = self.dict_size + 1
        self.dict_size += 1
        self.term_dictionary[word] = val
        self.reverse_term_dict[val] = word

    # TODO important note that we will want to do *exactly* the same operations within the NN when analyzing songs
    def _sanitize_word(self, word):
        return word.translate(self.word_sanitizer_table)\
            .lower()\
            .strip("'\t\r\n")  # we strip ' here along with whitespace to avoid removing punctuation *in* the word


# ------------------------------------------------------------------
# MANUAL TEST FUNCTIONS
# ------------------------------------------------------------------

# TODO big one -- we should probably figure out python unit testing...

def test_reader_one_file(sample_dir="", sample_song=""):
    reader = SongReader()
    directory = sample_dir if sample_dir else "sample-lyric-set"
    song_file = sample_song if sample_song else "big-poppa.txt"
    path = os.path.join(DATA_DIR, *['lyric-sets', directory, song_file])
    reader.read_file(path)
    print(reader.songs[0].text)
    _print_dicts(reader.term_dictionary, reader.reverse_term_dict)


def test_batch_read(sample_dir=""):
    reader = SongReader()
    test_dir = sample_dir if sample_dir else "sample-lyric-set"
    directory = os.path.join(DATA_DIR, *['lyric-sets', test_dir])
    reader.batch_read_files(directory)
    print("{} songs processed and stored".format(len(reader.songs)))
    _print_dicts(reader.term_dictionary, reader.reverse_term_dict)


def _print_dicts(term_dict, reverse_dict):
    for i in range(len(reverse_dict)):
        word_mapped_to_i = reverse_dict[i]
        if i % 10 == 0:
            print("-" * 40)
            print(" dict  | {:<20}  {}".format("key", "val"))
            print("-" * 40)
        print("term   | {:<20}: {}".format(word_mapped_to_i, term_dict[word_mapped_to_i]))
        print("r_term | {:<20}: {}".format(i, word_mapped_to_i))

# running tests...
test_reader_one_file(sample_song="express-yourself.txt")
#test_batch_read("nas-discography")
