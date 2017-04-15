import tkinter as tk
import os.path
from paths import *

from app.src.core.cranium import Cranium
from app.src.core.models.lstm_rnn import LstmRnn
from app.src.file.song_feed import SongFeed

from app.src.domain.default_char_index import *

class RprimeGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

        self.cranium = Cranium()

        self.feed = None

    def create_widgets(self):
        #Insert Model into Cranium Object Button
        self.insert_model_btn = tk.Button(self, text="Insert Model", command=self.insert_model)
        self.insert_model_btn.pack(side="top")

        #Train Model
        self.train_model_btn = tk.Button(self, text="Train Model", command=self.train_model_gui)
        self.train_model_btn.pack(side="top")

        #Spit Lyrics
        self.spit_btn = tk.Button(self, text="Spit", command=self.spit_gui)
        self.spit_btn.pack(side="top")

        #Exit the program
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def insert_model(self):
        #model = a_model
        #cranium.init_model(model)
        print("Start Insert")
        char_idx = create_char_index()
        model = LstmRnn(char_idx)
        self.cranium.init_model(model)
        print("Model Inserted into Cranium")

    def train_model_gui(self):
        print("Starting Train Model")
        self._build_feed()
        X, Y = self.feed.get_seq_data()
        data = {'X':X, 'Y':Y}
        self.cranium.train_model(data)
        print("Model Trained")

    #Helper Method for train_model
    #TODO file_path
    def _build_feed(self, file_path='gui-test'):

        self.feed = SongFeed.from_lyrics_directory(os.path.join(
            LYRICS_SETS, file_path
        ))

    def spit_gui(self):
        output = self.cranium.spit()
        print(output)

root = tk.Tk()
app = RprimeGui(master=root)
app.mainloop()
