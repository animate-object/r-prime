from app.src.gui.gui import main as run_gui
import os.path

from app.src.repository.script_runner import init_db
from paths import DATA_DIR


def main():
    expected_db_path = os.path.join(DATA_DIR, 'words', 'word.db')
    if not os.path.exists(expected_db_path):
        print("Word database not found, performing first time DB initialization.")
        print("This might take a moment")
        init_db()
    run_gui()

if __name__ == '__main__':
    main()
