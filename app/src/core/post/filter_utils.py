
def _strip_and_save_pad(word):
    """
    :param word: a word with or without punctuation
    :return: a tuple of left pad punctuation, right pad punctuation, and the word
    """
    word, r_pad = _strip_and_return_punctuation(word, right=True)
    word, l_pad = _strip_and_return_punctuation(word, right=False)
    return l_pad, r_pad, word


def _strip_and_return_punctuation(word, right=True, punctuation=None):
    """
    strip punctuation and return stripped string
    :param word:
    :return:
    """
    punctuation = '".,!;)].,!([?'
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
