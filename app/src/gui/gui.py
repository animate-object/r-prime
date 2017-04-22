import tkinter as tk

import os.path
from paths import *

from app.src.core.cranium import Cranium
from app.src.core.models.lstm_rnn import LstmRnn
from app.src.core.models.experimental_rnn_configs import *
from app.src.file.song_feed import SongFeed

from app.src.domain.default_char_index import *


NN_OPTIONS = {"LSTM RNN":LstmRnn, "Hot Dog RNN":HotDogRnn, "Jumbo Dog RNN":JumboDogRnn, "Hamburger RNN":HamburgerRnn}

class Gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Raptimus Prime")
        self.pack(fill=tk.BOTH, expand=1)
        self.select = 0
        self.cranium = Cranium()
        self.feed = None
        self.fire = None
        self.model_inserted = False
        self.startVar = tk.IntVar()
        #self.modelVar = tk.IntVar()
        self.modelStrVar = tk.StringVar()
        self.tempVar = tk.DoubleVar()

        #This array is for any widget that doesn't have a fixed value
        self.widgets = []

        self.create_widgets()


    def create_widgets(self, initStart=True):
        #Set up
        x = [20]
        y = [10]

        self.G = x
        self.H = y

        for i in range(0, 15):
            y.append(y[i] + 30)
            x.append(x[i] + 110)

        b = 0
        # Row - Make and load radio buttons
        if initStart == True:
            self.startRadioB1 = tk.Radiobutton(self, text="Make model", variable=self.startVar, value=0, command=self.changeMode)
            self.startRadioB1.place(x=x[1], y=y[b])

            self.startRadioB2 = tk.Radiobutton(self, text="Use Pre-trained Model", variable=self.startVar, value=1, command=self.changeMode)
            self.startRadioB2.place(x=x[2], y=y[b])

            self.feedbackLabel = tk.Label(self, text="Welcome to Raptimus Prime!")
            self.feedbackLabel["text"] = "Welcome?"
            self.feedbackLabel.place(x=x[4], y=y[b])

            self.outputWindow = tk.Text(self, width=50, height=20, wrap=tk.WORD)
            self.outputWindow.place(x=x[3], y=y[b+1])
        b +=1

        if (self.select == 0):
            self.createModelSelection(x, y, b)
        else:
            self.createEndWidgets(x, y, b)

    def createBodyWidgets(self, x, y, b):
        # Row - Load button + Entry
        #self.loadButton = tk.Button(self, text="Load", command=self.insert_model, width=10)
        #self.loadButton.place(x=x[0], y=y[b])
        self.pathEntry = tk.Entry(self, width=25)
        self.pathEntry.place(x=x[1], y=y[b])
        b += 1

        self.widgets.append(self.pathEntry)

        if (self.select == 0):
            self.createModelSelection(x, y, b)
        else:
            self.createEndWidgets(x, y, b)

    ###DONE###
    def createModelSelection(self, x, y, b):

        self.modelStrVar.set("Choose RNN")
        self.optionmenu = tk.OptionMenu(self, self.modelStrVar, *NN_OPTIONS.keys())
        self.optionmenu.place(x=x[1],y=y[b])

        self.modelLabel = tk.Label(self, text="Select a RNN")
        self.modelLabel.place(x=x[0], y=y[b])
        b+=1
        self.loadButton = tk.Button(self, text="Load", command=self.load_model, width=10)
        self.loadButton.place(x=x[0], y=y[b])

        """
        # Row of models
        self.lstmRnnButton = tk.Radiobutton(self, text="Lstm", variable=self.modelVar, value=0,
                                           command=self.changeModel)
        self.lstmRnnButton.place(x=x[1], y=y[b])
        self.hotDogRnnButton = tk.Radiobutton(self, text="HotDog", variable=self.modelVar, value=1,
                                             command=self.changeModel)
        self.hotDogRnnButton.place(x=x[2], y=y[b])
        self.jumboDogRnnButton = tk.Radiobutton(self, text="JumboDog", variable=self.modelVar, value=2,
                                               command=self.changeModel)
        self.jumboDogRnnButton.place(x=x[3], y=y[b])
        b+= 1
        # New row of models
        self.hamburgerRnnButton = tk.Radiobutton(self, text="Hamburger", variable=self.modelVar, value=3,
                                                command=self.changeModel)
        self.hamburgerRnnButton.place(x=x[1], y=y[b])
        self.pancakeRnnButton = tk.Radiobutton(self, text="Pancake", variable=self.modelVar, value=4,
                                                 command=self.changeModel)
        self.pancakeRnnButton.place(x=x[2], y=y[b])
        self.pizzaDoughRnnButton = tk.Radiobutton(self, text="PizzaDough", variable=self.modelVar, value=5,
                                               command=self.changeModel)
        self.pizzaDoughRnnButton.place(x=x[3], y=y[b])
        b += 1
        
        self.widgets.append(self.modelLabel)
        self.widgets.append(self.loadButton)
        self.widgets.append(self.lstmRnnButton)
        self.widgets.append(self.hotDogRnnButton)
        self.widgets.append(self.jumboDogRnnButton)
        self.widgets.append(self.hamburgerRnnButton)
        self.widgets.append(self.pancakeRnnButton)
        self.widgets.append(self.pizzaDoughRnnButton)
        """

        self.widgets.append(self.loadButton)
        self.widgets.append(self.optionmenu)
        self.createTrainWidgets(x, y, b)

    def createTrainWidgets(self, x, y, b):
        # Row - Train button + feedback
        b += 1
        self.trainButton = tk.Button(self, text="Train", command=self.train_model_gui, width=10)
        self.trainButton.place(x=x[0], y=y[b])
        self.epochLabel = tk.Label(self, text = "Epochs to train:")
        self.epochLabel.place(x=x[1], y=y[b])
        self.epochEntry = tk.Entry(self, width= 6)
        self.epochEntry.place(x=x[2], y=y[b])
        b += 1
        self.saveModelButton = tk.Button(self, text="Save Model", command=self.save_model, width=10)
        self.saveModelButton.place(x=x[0], y=y[b])
        self.pathLabel = tk.Label(self, text = "Training data path:")
        self.pathLabel.place(x=x[1], y=y[b])
        self.pathEntry = tk.Entry(self, width=25)
        self.pathEntry.place(x=x[2], y=y[b])
        b+= 1

        #self.trainLabel = tk.Label(self)  # , textvariable=StringVar())
        #self.trainLabel.place(x=x[1], y=y[b])
        #b += 1
        #Append and continue
        self.widgets.append(self.pathLabel)
        self.widgets.append(self.pathEntry)
        self.widgets.append(self.saveModelButton)
        self.widgets.append(self.epochLabel)
        self.widgets.append(self.epochEntry)
        self.widgets.append(self.trainButton)
        self.createSpitWidgets(x, y, b)

    def createSpitWidgets(self, x, y, b):
        # Row - Spit button + feedback
        b += 1
        self.spitButton = tk.Button(self, text="Spit", command=self.spit_gui, width=10)
        self.spitButton.place(x=x[0], y=y[b])
        self.tempLabel = tk.Label(self, text="Temperature:")
        self.tempLabel.place(x=x[1], y=y[b])
        self.tempEntry = tk.Entry(self, width=6)
        self.tempEntry.place(x=x[2], y=y[b])
        b +=1
        self.saveFireButton = tk.Button(self, text="Save Spit", command=self.save_fire, width=10)
        self.saveFireButton.place(x=x[0], y=y[b])
        #self.tempScale = tk.Scale(self, variable = self.tempVar, from_=0.0, to=1.0, width=25, orient=tk.HORIZONTAL, resolution=0.01)
        #self.tempScale.place(x=x[2], y=y[b-1])
        # self.spitLabel = tk.Label(self)
        # self.spitLabel.place(x=x[1], y=y[b])
        b += 1


        self.widgets.append(self.tempLabel)
        self.widgets.append(self.tempEntry)
        self.widgets.append(self.spitButton)
        self.widgets.append(self.saveFireButton)
        self.createEndWidgets(x, y, b)

    def createEndWidgets(self, x, y, b):
        # Row - Quit button
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.place(x=x[0], y=y[b+1])
        self.widgets.append(self.quit)
        # self.refresh()

    def changeModel(self):
        modelInfo = [
            "Default LstmRnn",
            "Deep but wide LstmRnn",
            "Deep but wider LstmRnn",
            "Wide, shallow network",
            "Wide, very shallow network",
            "Very wide, very shallow network"
            ]
        self.modelLabel["text"] = modelInfo[self.modelVar.get()]

    def changeMode(self):
        if (self.select == self.startVar.get()):
            return
        self.select = self.startVar.get()
        self.reset(self.select)
        self.create_widgets(False)

    # Insert Model helper method
    def load_model(self):
        self.insert_model(self.modelStrVar.get())

    def insert_model(self, choice=None):

        print("Start Insert")
        print(choice)
        char_idx = create_char_index()
        model = NN_OPTIONS[choice]
        self.cranium.init_model(model(char_idx))

        print("Model Inserted into Cranium")

    def train_model_gui(self):
        print("Starting Train Model")
        self._build_feed(self.pathEntry.get())
        X, Y = self.feed.get_seq_data()
        data = {'X':X, 'Y':Y}
        for iters in range(int(self.epochEntry.get())):
            self.cranium.train_model(data, params={'epochs': 1, 'batch_size': 128})
        print("Model Trained")

    # Helper Method for train_model
    # TODO file_path
    def _build_feed(self, a_data_dir):
        self.feed = SongFeed.from_lyrics_directory(os.path.join(
            LYRICS_SETS, a_data_dir
        ))

    # Clears widgets to set them up again
    def reset(self, mode=0):
        self.cranium = Cranium()
        self.feed = None
        self.fire = None
        self.model_inserted = False

        for i in range(len(self.widgets)):
            self.widgets[i].destroy()

        self.widgets = []

    def spit_gui(self):
        self.fire = self.cranium.spit(temp=float(self.tempEntry.get()))
        self.outputWindow.insert(tk.END, self.fire)
        print(self.fire)

    def save_fire(self):
        None

    def save_model(self):
        None

root = tk.Tk()
root.geometry("800x400+300+300")
app = Gui(master=root)
app.mainloop()
