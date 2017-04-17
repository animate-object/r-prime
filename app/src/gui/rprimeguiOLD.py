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

        #Create the pieces of the interface
        self.create_widgets()

        #Instantiate the Cranium
        self.cranium = Cranium()

        #Song Feed variable
        self.feed = None

    """
    Creates all of the things inside the window
    """
    def create_widgets(self):

        #Insert Model into Cranium Object Button
        self.insert_model_btn = tk.Button(self, text="Insert Model", command=self.insert_model)
        self.insert_model_btn.pack(side="left")

        #Train Model
        self.train_model_btn = tk.Button(self, text="Train Model", command=self.train_model_gui)
        self.train_model_btn.pack(side="left")

        #Spit Lyrics
        self.spit_btn = tk.Button(self, text="Spit", command=self.spit_gui)
        self.spit_btn.pack(side="left")

        #Save State
        self.save_btn = tk.Button(self, text="Save Model", command=self.save_state_gui)
        self.save_btn.pack(side="left")

        #Load State
        self.load_btn = tk.Button(self, text="Load Model", command=self.load_state_gui)
        self.load_btn.pack(side="left")

        #Text Window
        self.output_window = tk.Text(self, state="disabled")
        self.output_window.pack(side="right")

        #Exit the program
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    """
    Inserts a model into the Cranium object
    """
    def insert_model(self):
        #model = a_model
        #cranium.init_model(model)
        print("Start Insert")
        char_idx = create_char_index()
        model = LstmRnn(char_idx)
        self.cranium.init_model(model)
        print("Model Inserted into Cranium")
    """
    Trains the current model
    """
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
    """
    Generates the output text
    """
    def spit_gui(self):
        print("Getting Output")
        output = self.cranium.spit()
        ##########self.output_window.insert(self,1.0,"Some Text")
        print(output)

    def save_state_gui(self, path):
        pass

    def load_state_gui(self, path):
        pass

root = tk.Tk()
root.geometry("800x500+300+100")
app = RprimeGui(master=root)
app.mainloop()