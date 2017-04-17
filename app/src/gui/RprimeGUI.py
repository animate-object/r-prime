from tkinter import *
from app.src.core.cranium import Cranium
import os.path
from paths import *
from app.src.file.song_feed import SongFeed

from app.src.domain.default_char_index import *

from app.src.core.models.lstm_rnn import LstmRnn
from app.src.core.models.experimental_rnn_configs import *

class RprimeGUI:

    def __init__(self, master):
        #Class Variables
        self.cranium = Cranium()
        self.nn_selection = IntVar()
        self.train_path = StringVar()

        """GUI Widgets"""
        #Main Window
        main_frame = Frame(master)
        main_frame.pack(fill="both", expand="yes")

        #Left side of GUI
        left_frame = LabelFrame(main_frame)
        left_frame.pack(side=LEFT)

        #Right side of GUI
        right_frame = LabelFrame(main_frame)
        right_frame.pack(side=RIGHT)

        #Holds radio buttons and insert model button
        select_model_frame = LabelFrame(left_frame, text="Select Model")
        select_model_frame.pack(side=TOP)

        #Holds Train Model things
        train_frame = LabelFrame(left_frame, text="Train Model")
        train_frame.pack(side=TOP)

        #Holds save and load buttons
        sl_frame = LabelFrame(left_frame, text = "Save and Load")
        sl_frame.pack(side=TOP)

        #Radio buttons for selecting NNs
        Radiobutton(select_model_frame,text="LSTM RNN", variable=self.nn_selection, value=1,
                    command=self.rbtest).pack(side=TOP)
        Radiobutton(select_model_frame, text="Hot Dog RNN", variable=self.nn_selection, value=2,
                    command=self.rbtest).pack(side=TOP)
        Radiobutton(select_model_frame, text="Jumbo Dog RNN", variable=self.nn_selection, value=3,
                    command=self.rbtest).pack(side=TOP)
        Radiobutton(select_model_frame, text="Hamburger RNN", variable=self.nn_selection, value=4,
                    command=self.rbtest).pack(side=TOP)

        #Button to insert model into cranium
        self.insert_model_button = Button(select_model_frame, text="Insert Model", command=self.insert_model)
        self.insert_model_button.pack(side=TOP)

        #Text Box for train_path
        self.train_path_entry = Entry(train_frame,
                                      textvariable=self.train_path)
        self.train_path_entry.pack(side=TOP)

        #Button to train model
        self.train_model_button = Button(train_frame,text="Train Model",
                                         command=self.train_model_gui)
        self.train_model_button.pack(side=TOP)

        #Button to spit output
        self.spit_button = Button(left_frame,text="Spit",command=self.spit_gui)
        self.spit_button.pack(side=TOP)

        #Save Button
        self.save_button = Button(sl_frame, text="Save", command=self.save_state_gui)
        self.save_button.pack(side=LEFT)

        #Load Button
        self.load_button = Button(sl_frame, text="Load", command=self.load_state_gui)
        self.load_button.pack(side=LEFT)

        #Output window
        self.output_window = Text(right_frame, wrap=WORD)
        self.output_window.pack(side=TOP)

        quit_btn = Button(left_frame,text="QUIT",fg="red", command=main_frame.quit)
        quit_btn.pack(side=BOTTOM)

    """
    Tests the radio buttons
    """
    def rbtest(self):
        print(self.nn_selection.get())

    """
    Choose the model corresponding to the number given by
    the radio buttons
    """
    def insert_model(self):
        print("Inserting Model")
        char_idx = create_char_index()
        if(self.nn_selection.get()==1):
            model = LstmRnn(char_idx)
            self.cranium.init_model(model)
            print("LSTM RNN Selected")
        elif(self.nn_selection.get()==2):
            model = HotDogRnn(char_idx)
            self.cranium.init_model(model)
            print("Hot Dog RNN Selected")
        elif (self.nn_selection.get() == 3):
            model = JumboDogRnn(char_idx)
            self.cranium.init_model(model)
            print("Jumbo Dog RNN Selected")
        elif (self.nn_selection.get() == 4):
            model = HamburgerRnn(char_idx)
            self.cranium.init_model(model)
            print("Hamburger RNN Selected")
        else:
            model = LstmRnn(char_idx)
            self.cranium.init_model(model)
            print("Default RNN Selected")

        print(self.nn_selection.get())
        print("Model Inserted")

    def train_model_gui(self, a_data_dir=None):
        a_data_dir = self.train_path.get()
        print("Starting Train Model")
        print(a_data_dir)
        self._build_feed(a_data_dir)
        X, Y = self.feed.get_seq_data()
        data = {'X': X, 'Y': Y}
        self.cranium.train_model(data)
        print("Model Trained")

    # Helper Method for train_model
    # TODO file_path
    def _build_feed(self, a_data_dir):
        self.feed = SongFeed.from_lyrics_directory(os.path.join(
            LYRICS_SETS, a_data_dir
        ))

    def spit_gui(self):
        print("Getting Output")
        output = self.cranium.spit()
        self.output_window.insert(END, output)
        #print(output)
        print("Output Done")

    def save_state_gui(self):
        pass

    def load_state_gui(self):
        pass



#Testing

def main():
    root = Tk()
    app = RprimeGUI(root)
    root.mainloop()
    root.destroy()

main()
