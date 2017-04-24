import random

from app.src.core.post.filter_utils import _strip_and_save_pad
from app.src.repository.db_queries import find_word, find_similar_words


def remove_nonsense_words(text, highlight_replacements=False):
    output = ''
    for line in text.split('\n'):
        line = remove_nonsense_words_from_line(line, highlight_replacements)
        output += line
    return output


def remove_nonsense_words_from_line(line, highlight_replaced_words):
    ret = []
    line = line.rstrip('\n').split()
    for word in line:
        left_pad, right_pad, word = _strip_and_save_pad(word)
        print(word)
        is_cap = word[0].isupper() if word else False
        word = word.lower()
        # if the word is a nonsense word
        if not find_word(word):
            word = find_like_word(word)
            word = word.capitalize() if is_cap else word
            if highlight_replaced_words:
                word = "<" + word + ">"
        else:
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


# TEST

