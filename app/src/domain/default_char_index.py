"""
It would be nice to support unicode etc but for now we're just going to enforce this default, ascii only
character index
"""
from string import printable


def create_char_index():
    # corresponds to the set of ascii printable characters
    return {char: i for (i, char) in enumerate(printable)}
