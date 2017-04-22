import sqlite3 as sql
import os.path
from string import printable

from paths import DATA_DIR

WORD_DB_PATH = os.path.join(DATA_DIR, "words", "words.db")
WORD_SRC_PATH = os.path.join(DATA_DIR, "words", "words.txt")


def is_word_query(possible_word):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words WHERE word =?', (possible_word.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result


def word_like_query(non_word,max_results=10):
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words WHERE word LIKE ?', ("%"+non_word.lower()+"%",))
    result = cursor.fetchmany(max_results)
    conn.commit()
    conn.close()
    return [tup[0] for tup in result]


def init_word_db():
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE words
            (word TEXT PRIMARY KEY)
        '''
    )
    conn.commit()
    conn.close()


def populate_word_db():
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()

    with open(WORD_SRC_PATH, 'r') as words:
        for line in words:
            word = str(line.strip('\n'))
            try:
                # right now we're not going to mess with non ascii words
                if word and _is_ascii(word):
                    # print('inserting word {}'.format(word))
                    cursor.execute('''INSERT INTO words VALUES (?)''', (word,))
            except sql.IntegrityError as e:
                print(e)
                print("DUPLICATE ENTRY {}".format(word))
    conn.commit()
    conn.close()


def what_is_even_in_here():
    conn = sql.connect(WORD_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words")
    result = cursor.fetchmany(1000)
    # conn.commit()
    conn.close()
    return result


def _is_ascii(word):
    for letter in word:
        if letter not in printable:
            return False
    return True


def db_start_up():
    init_word_db()
    populate_word_db()


# db_start_up()

print(word_like_query('bc'))
