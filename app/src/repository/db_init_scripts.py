import sqlite3 as sql
import os.path
import re


from paths import DATA_DIR

WORD_DB_PATH = os.path.join(DATA_DIR, 'words', 'word.db')
CMU_SRC_PATH = os.path.join(DATA_DIR, 'words', 'cmudict.dict')
CMU_PHONES = os.path.join(DATA_DIR, 'words', 'cmudict.phones')

"""
TABLE DEFINITION NOTES
We store only up to the last three syllables of the word because these are the most interesting
when determining rhyming properties. For now we store stress data in case we care about it later.

ult - ultimate (last)
pult - penultimate (second from last)
apult - antepenultimate (third from last)

rime - the part of syllable including its nucleus (vowel sound) and coda (terminal consonant sound) if it exists
the rime is (perhaps not coincidentally) what determines if two syllables rhyme.

E.g., cat and bat are both one syllable words that differ in their *onset* but share a rime
"""
CREATE_WORDS_TABLE = '''
CREATE TABLE words (
    word TEXT NOT NULL,
    variation_num INTEGER NOT NULL DEFAULT 0,
    syl_ult TEXT,
    syl_pult TEXT,
    syl_apult TEXT,
    rime_ult TEXT,
    rime_pult TEXT,
    rime_apult TEXT,
    syl_count INTEGER,
    stress_primary INTEGER,
    stress_secondary INTEGER,
    PRIMARY KEY (word, variation_num)
);
'''


def init_word_table():
    if os.path.isfile(WORD_DB_PATH):
        os.remove(WORD_DB_PATH)
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(CREATE_WORDS_TABLE)
    conn.commit()
    conn.close()


def populate_word_table_with_cmudict_entries():
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    with open(CMU_SRC_PATH, 'r') as dict_in:
        for line in dict_in:
            if not line.startswith("#"):
                try:
                    entry_vals = parse_cmu_entry(line)
                    cursor.execute("INSERT INTO words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entry_vals)
                except sql.IntegrityError as e:
                    print(e)
                    print("failed insert vals:\n{}".format(line))
    conn.commit()
    conn.close()


def check_contents(n):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words")
    results = cursor.fetchmany(n)
    conn.commit()
    return results

# ---------------------------------------
# functions for working with the CMUDICT
# ---------------------------------------

# This list is ordered from most to least common
# vowels in terms of appearances in the CMU dict
CMU_VOWELS = [
    'AH', 'ER', 'IH',
    'IY', 'EH', 'AA',
    'AE', 'OW', 'EY',
    'AY', 'AO', 'UW',
    'AW', 'UH', 'OY'
]


def parse_cmu_entry(line):
    """
    From each entry in the CMU dictionary we need to extract values for all of our columns
    for the express purpose of easy storage in our database, we will output this as a tuple that can be
    inserted into the words table directly
    :param line one row from the cmudict.dict file
    """

    line_data = line.split()
    word_part, syl_part = line_data[0], line_data[1:]

    return get_word_and_variation(word_part) + get_syllables_and_stress(syl_part)


def get_word_and_variation(word_part):
    """
    :param word_part:
    :return: the word and the variation number if present
    """
    var_num = re.search("\((.*)\)", word_part)
    if var_num:
        word = word_part[:-3]  # trim off the (n) from the end of the entry
        var_num = int(var_num.group(1))
    else:
        var_num = 1
        word = word_part
    return word, var_num


def get_syllables_and_stress(syllable_part):
    """
    :param syllable_part:
    :return: tuple of all the syllable and stress data for that entry
    """
    syllables = []
    cur_syl = ''
    primary_stress, sec_stress = None, None
    for phoneme in syllable_part:
        if phoneme == '-':
            syllables.append(cur_syl)
            cur_syl = ''
            continue
        cur_syl += phoneme
    syllables.append(cur_syl)

    # determine stress
    for i, syl in enumerate(syllables):
        stress = re.search('\d', syl)
        syllables[i] = re.sub('\d', '', syl)
        stress = stress.group() if stress else 0
        if stress == '1':
            primary_stress = i
        elif stress == '2':
            sec_stress = i
    ult_syl = syllables[-1]
    pult_syl = syllables[-2] if len(syllables) > 1 else None
    apult_syl = syllables[-3] if len(syllables) > 2 else None
    ult_rime = strip_onset(ult_syl)
    pult_rime = strip_onset(pult_syl) if pult_syl else None
    apult_rime = strip_onset(apult_syl) if apult_syl else None

    return (ult_syl, pult_syl, apult_syl,
            ult_rime, pult_rime, apult_rime,
            len(syllables), primary_stress, sec_stress)


def strip_onset(syllable):
    for vowel in CMU_VOWELS:
        start_rime = syllable.find(vowel)
        if start_rime >= 0:
            return syllable[start_rime:]

sample_cmu_line1 = "GEOLOGISTS(2)  JH IY0 - AA1 - L AH0 - JH IH0 S S"
sample_cmu_line2 = "DENIED  D IH0 - N AY1 D"
sample_cmu_line3 = "MOBILIZATION(2)  M OW2 - B AH0 - L IH0 - Z EY1 - SH AH0 N"

# print(parse_cmu_entry(sample_cmu_line2))
# print(parse_cmu_entry(sample_cmu_line3))

print(strip_onset('SHAHN'))
print(strip_onset('NAYD'))
print(strip_onset('DIH'))
print(strip_onset('PRIHNS'))
