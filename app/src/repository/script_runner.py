from app.src.repository.db_init_scripts import *


def init_db():
    init_word_table()
    populate_word_table_with_cmudict_entries()

if __name__ == '__main__':
    init_db()
    [print(entry) for entry in check_contents(100)]
