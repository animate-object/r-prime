from paths import DATA_DIR
import os.path


class SongReader:
    def __init__(self, path=""):
        self.term_dictionary = {"<!PLACEHOLDER>": 0}
        self.reverse_term_dict = {0: "<!PLACEHOLDER>"}
        self.songs = []
        self.line_sanitizer_table = str.maketrans("", "", "(),?&;\"")  # table to remove line punctuation with str.translate
        self.word_sanitizer_table = str.maketrans("", "", "{}*-:!.,<>&")

    def read_file(self, path_to_song):
        # actually read in the file
        # parse the file line by line and add to term_dictionary & reverse_term_dictionary
        # store the file text in the songs
        with open(path_to_song, "r", encoding="utf-8") as fileIn:
            song = ""

            for line in fileIn:
                # we may want to other things in these cases in the future.
                if line.startswith("[") or line.startswith("#") or line.startswith("~"):
                    continue
                else:
                    song += self._parse_line(line)
            self.songs.append(song)

    def batch_read_files(self, path_to_folder):
        all_contents = [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder)]
        text_file_paths = [f for f in all_contents if os.path.isfile(f) and f.endswith(".txt")]
        print()
        for file_path in text_file_paths:
            self.read_file(file_path)

    def _add_word_to_dicts(self, word):
        val = max(self.reverse_term_dict.keys()) + 1
        self.term_dictionary[word] = val
        self.reverse_term_dict[val] = word

    def _parse_line(self, line):
        line = line.translate(self.line_sanitizer_table)
        for word in line.split():
            word = word.translate(self.word_sanitizer_table)
            word = word.lower().strip("' ")
            if word and word not in self.term_dictionary:
                self._add_word_to_dicts(word)
        return line


# ------------------------------------------------------------------
# MANUAL TEST FUNCTIONS
# ------------------------------------------------------------------


def test_reader_one_file(sample_dir="", sample_song=""):
    reader = SongReader()
    directory = sample_dir if sample_dir else "sample-lyric-set"
    song_file = sample_song if sample_song else "big-poppa.txt"
    path = os.path.join(DATA_DIR, *['lyric-sets', directory, song_file])
    reader.read_file(path)
    print(reader.songs[0])
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
            print(" dict  | {:<20}  {}".format("key","val"))
            print("-" * 40)
        print("term   | {:<20}: {}".format(word_mapped_to_i, term_dict[word_mapped_to_i]))
        print("r_term | {:<20}: {}".format(i, word_mapped_to_i))

# running tests...
# test_reader_one_file(sample_song="express-yourself.txt")
# test_batch_read("nas-discography")
