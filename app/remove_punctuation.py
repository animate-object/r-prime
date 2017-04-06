from string import punctuation

remove_punctuation_table = str.maketrans('', '', punctuation)

def remove_punctuation_from_file(file_path):
    with open(file_path, 'r+') as fin:
        text = fin.read()
        text = text.translate(remove_punctuation_table)
