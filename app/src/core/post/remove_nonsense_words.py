import random

from app.src.repository.db_queries import find_word, find_similar_words


def remove_nonsense_words(text):
    output = ''
    for line in text.split('\n'):
        line = remove_nonsense_words_from_line(line)
        output += line
    return output


def remove_nonsense_words_from_line(line):
    ret = []
    line = line.rstrip('\n').split()
    for word in line:
        left_pad, right_pad, word = _strip_and_save_pad(word)
        is_cap = word[0].isupper()
        word = word.lower()
        # if the word is a nonsense word
        if not find_word(word):
            word = find_like_word(word)
        word = word.capitalize() if is_cap else word
        word = left_pad + word + right_pad

        ret.append(word)
    return ' '.join(ret) + '\n'


def find_like_word(nonsense_word):
    close_matches = []
    while len(close_matches) == 0:
        close_matches = find_similar_words(nonsense_word)
        nonsense_word = nonsense_word[:-1]
    return random.choice(close_matches)


def _strip_and_save_pad(word):
    word, r_pad = _strip_and_return_punctuation(word, right=True)
    word, l_pad = _strip_and_return_punctuation(word, right=False)
    return l_pad, r_pad, word


def _strip_and_return_punctuation(word, right=True, punctuation=None):
    """
    strip punctuation and return stripped string
    :param word:
    :return:
    """
    default_punctuation = '".,!;)]' if right else '".,!(['
    punctuation = punctuation if punctuation else default_punctuation
    stripped = ''
    word = reverse_word(word) if right else word
    for c in word:
        if c in punctuation:
            stripped += c
            word = word[1:]
        else:
            break
    word = reverse_word(word) if right else word
    stripped = reverse_word(stripped) if right else stripped
    return word, stripped


def reverse_word(word):
    return word[::-1]

# TEST
sample_word = '"You."'

sample_text = """
"Henlo mah num iz g unit tmo gizzar (bloccc)!"
"""

print(remove_nonsense_words(sample_text))
