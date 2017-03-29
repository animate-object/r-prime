from app.src.domain.song import Song
from paths import DATA_DIR
import os.path

# FIXME not sure this class has a place in the current app architecture
# if it does, it will be leveraging the reader function in file utils to store songs...
# don't use this class for now
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


def tokenize_text(text, seq_sanitize_tbl=None, tokenize_fn=None):
    word_san = str.maketrans("", "", "-")

    # TODO remove duplicated code
    def sanitize_word(word):
        return word.translate(word_san)\
            .lower()\
            .strip("'")  # we strip ' here along with whitespace to avoid removing punctuation *in* the word

    seq_sanitize_tbl = seq_sanitize_tbl if seq_sanitize_tbl else str.maketrans("", "", "{}*:!.,<>&(),?&;\"")
    tokenize = tokenize_fn if tokenize_fn else sanitize_word
    text = text.translate(seq_sanitize_tbl)
    tokenized = []

    for word in text.split(' '):
        word = tokenize(word)
        newline = word.find('\n') + 1
        if newline > 0:
            word_1 = word[:newline]
            word_2 = word[newline:]
            tokenized += [word_1, word_2]
        else:
            tokenized.append(word)

    return tokenized


def word_sequence_to_X_Y(text, subseq_len):
    """
    :param text: your text... will be sanitized and tokenized with default functions if none are provided
    :param subseq_len: how many words long do you want each X sequence to be (at maximum)... should probably be shorter
    than the total length of your text.

    :return: (X, Y) where
    X is an array of x_n where each x is an array of consecutive words from the sequence starting at n
    Y is an array of y_n where each y is the word that follows the sub_sequence x from the text
        There is a one to one correspondence of X -> Y e.g.
        Text = "life's a bitch and then you die . . . " subseq_len = 4
        x_1 -> y_1 || X[1] -> Y[1]: ["life's", "a", "bitch", "and"] -> "then"
        x_2 -> y_2 || X[2] -> Y[2]: ["a", "bitch", "and", "then"] -> "you"
        . . . etc
        """
    text = tokenize_text(text=text)
    X = []
    Y = []

    for x_start in range(0, len(text) - subseq_len):
        y_idx = x_start + subseq_len
        X.append(text[x_start:y_idx])
        Y.append(text[y_idx])
    return X, Y


def char_sequence_to_X_Y(text, subseq_len):
    """ X is an array of x_n where each x is a string of consecutive letters from the sequence starting at n
        Y is an array of y_n where each y is the character that follows the string x from the sequence
        :param text:
        :param subseq_len:
    """
    X = []
    Y = []

    for x_start in range(0, len(text) - subseq_len):
        y_idx = x_start + subseq_len
        X.append(text[x_start:y_idx])
        Y.append(text[y_idx])
    return X, Y

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
# test_reader_one_file(sample_song="express-yourself.txt")
# test_batch_read("nas-discography")
