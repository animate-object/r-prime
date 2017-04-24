from app.src.repository.db_init_scripts import *


def init_db():
    print("Initializing syllabic word database for rhyming.")
    init_word_table()
    print("Populating word database with entries from CMU syllabic dictionary.")
    populate_word_table_with_cmudict_entries(CMU_SRC_PATH)
    print("Making it dank.")
    populate_word_table_with_cmudict_entries(CMU_HIP_HOP)

if __name__ == '__main__':
    init_db()
    # [print(entry) for entry in check_contents(100)]
