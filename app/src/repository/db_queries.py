"""
Queries against the word database, wrapped for use elsewhere in the backend
"""

import sqlite3 as sql
import os.path

from paths import DATA_DIR

WORD_DB_PATH = os.path.join(DATA_DIR, 'words', 'word.db')


def find_word(word):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words WHERE word = (?)', (word.upper(),))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result


def find_similar_words(non_word, max_results=10, keep_first_letter=True):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    if keep_first_letter:
        query_param = (non_word.upper() + '%',)
    else:
        query_param = ('%' + non_word.upper() + '%',)
    cursor.execute('SELECT * FROM words WHERE word LIKE ?', query_param)
    result = cursor.fetchmany(max_results)
    conn.commit()
    conn.close()
    return [tup[0].lower() for tup in result]


def find_rhymes(word):
    word_entry = find_word(word)
    ult, pult, apult = word_entry[2], word_entry[3], word_entry[4]
    results = []
    results += find_1_syl_rhymes(ult)
    if pult:
        results += find_2_syl_rhymes(ult, pult)
    if apult:
        results += find_3_syl_rhymes(ult, pult, apult)
    return [result[0] for result in results if result[0] != word]


def find_rhymes_v2(word):
    """
    Given that more complete rhymes are often more pleasing to the ear, this method will return only
    the longest rhymes in terms of rhyming syllable count.
    :param word:
    :return: rhyming words or an empty list if no rhymes are found
    """
    word_entry = find_word(word)
    ult, pult, apult = word_entry[2], word_entry[3], word_entry[4]
    if apult:
        results = find_3_syl_rhymes(ult, pult, apult)
        if len(results) > 1:  # a results list of length one only contains the word we're trying to find rhymes for
            return results
    if pult:
        results = find_2_syl_rhymes(ult, pult)
        if len(results) > 1:
            return results
    return find_1_syl_rhymes(ult)


def find_rhymes_v3(word):
    """
    Similar to v2 except instead of checking against the syllables themselves for matches, we compare the
    rime part of each syllable. This allows, for instance Prince to rhyme with Convince (v2 would rhyme
    Prince with the imaginary word Conprince).
    We still prefer more complete matches to last part matches.
    :param word:
    :return:
    """
    word_entry = find_word(word)
    if not word_entry or len(word_entry) == 0:
        return []
    ult_rime, pult_rime, apult_rime, syl_count = word_entry[5], word_entry[6], word_entry[7], word_entry[8]
    if apult_rime and syl_count > 2:
        results = find_3_rime_matches(ult_rime, pult_rime, apult_rime)
        if len(results) > 1:
            return results
    if pult_rime and syl_count > 1:
        results = find_2_rime_matches(ult_rime, pult_rime)
        if len(results) > 1:
            return results
    return find_1_rime_matches(ult_rime)


def find_1_syl_rhymes(ult):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT word FROM words WHERE syl_ult = (?);''', (ult,))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def find_2_syl_rhymes(ult, pult):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT word FROM words WHERE syl_ult = (?) AND syl_penult = (?);''', (ult, pult))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def find_3_syl_rhymes(ult, pult, apult):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT word FROM words
        WHERE syl_ult = (?)
        AND syl_penult = (?)
        AND syl_antepenult = (?);
    ''', (ult, pult, apult))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def find_1_rime_matches(ult_rime):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT word FROM words
        WHERE rime_ult = (?)
    ''', (ult_rime,))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def find_2_rime_matches(ult_rime, pult_rime):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT word FROM words
        WHERE rime_ult = (?)
        AND rime_pult = (?)
    ''', (ult_rime, pult_rime))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def find_3_rime_matches(ult_rime, pult_rime, apult_rime):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT word FROM words
        WHERE rime_ult = (?)
        AND rime_pult = (?)
        AND rime_apult = (?)
    ''', (ult_rime, pult_rime, apult_rime))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

#
# test_words = ['truth','prince','dough','me','personally','projects','cops','money','chases']
#
# print("Looking for rhymes. . . ")
# for word in test_words:
#     print("Finding rhymes for: ", word)
#     print("Results: ", ', '.join([result[0] for result in find_rhymes_v3(word)]))
#     print("-" * 100)
