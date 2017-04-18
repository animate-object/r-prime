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
        self.startVar = tk.IntVar()
        #self.modelVar = tk.IntVar()
        self.modelStrVar = tk.StringVar()
        self.tempVar = tk.DoubleVar()

        #variables for what's loaded
        self.model_inserted = False
        self.model_trained = False
        self.fire = None

        #This array is for any widget that doesn't have a fixed value
        self.widgets = []
        self.feedback = ["", "", ""]
        self.create_widgets()
        self.giveFeedback("Welcome to R-Prime")

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
            self.createInitWidgets(x, y)
        b +=1

        if (self.select == 0):
            self.createModelSelection(x, y, b)
        else:
            self.createEndWidgets(x, y, b)

    #Create Initial Widgets that are never deleted and re-created
    def createInitWidgets(self, x, y):
        b = 0
        self.startRadioB1 = tk.Radiobutton(self, text="Make model", variable=self.startVar, value=0,
                                           command=self.changeMode)
        self.startRadioB1.place(x=x[1], y=y[b])

        self.startRadioB2 = tk.Radiobutton(self, text="Use Pre-trained Model", variable=self.startVar, value=1,
                                           command=self.changeMode)
        self.startRadioB2.place(x=x[2], y=y[b])

        self.outputWindow = tk.Text(self, width=55, height=20, wrap=tk.WORD)
        self.outputWindow.place(x=x[4], y=y[b + 1])

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

    def createModelSelection(self, x, y, b):
        b += 1
        self.modelStrVar.set("LSTM RNN")
        self.optionmenu = tk.OptionMenu(self, self.modelStrVar, *NN_OPTIONS.keys())
        #self.optionmenu["command"] = self.refresh
        self.optionmenu.place(x=x[2]-10,y=y[b]-2)

        self.modelLabel = tk.Label(self, text="Select a RNN")
        self.modelLabel.place(x=x[0], y=y[b])
        #b+=1
        self.loadButton = tk.Button(self, text="Load", command=self.load_model, width=9)
        self.loadButton.place(x=x[1], y=y[b])
        b+=1
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
        self.widgets.append(self.modelLabel)
        self.createTrainWidgets(x, y, b)

    def createTrainWidgets(self, x, y, b):
        # Row - Train button + feedback
        b += 1
        self.trainButton = tk.Button(self, text="Train", command=self.train_model_gui, width=9)
        self.trainButton.place(x=x[0], y=y[b])
        self.epochLabel = tk.Label(self, text = "Epochs to train:")
        self.epochLabel.place(x=x[1], y=y[b])
        self.epochEntry = tk.Entry(self, width= 6)
        self.epochEntry.place(x=x[2], y=y[b])
        b += 1
        self.saveModelButton = tk.Button(self, text="Save Model", command=self.save_model, width=9)
        self.saveModelButton.place(x=x[0], y=y[b])
        self.pathLabel = tk.Label(self, text = "Training data path:")
        self.pathLabel.place(x=x[1], y=y[b])
        self.pathEntry = tk.Entry(self, width=15)
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
        self.spitButton = tk.Button(self, text="Spit", command=self.spit_gui, width=9)
        self.spitButton.place(x=x[0], y=y[b])
        self.tempLabel = tk.Label(self, text="Temperature:")
        self.tempLabel.place(x=x[1], y=y[b])
        self.tempEntry = tk.Entry(self, width=6)
        self.tempEntry.place(x=x[2], y=y[b])
        b +=1
        self.saveFireButton = tk.Button(self, text="Save Spit", command=self.save_fire, width=9)
        self.saveFireButton.place(x=x[0], y=y[b])
        b += 1


        self.widgets.append(self.tempLabel)
        self.widgets.append(self.tempEntry)
        self.widgets.append(self.spitButton)
        self.widgets.append(self.saveFireButton)
        self.createEndWidgets(x, y, b)

    def createEndWidgets(self, x, y, b):
        # Row - Quit button
        feedbackX = 0
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.place(x=x[0], y=y[b])
        b += 1
        self.feedbackLabel0 = tk.Label(self, text="")
        self.feedbackLabel0.place(x=x[feedbackX], y=y[b])
        b += 1
        self.feedbackLabel1 = tk.Label(self, text="")
        self.feedbackLabel1.place(x=x[feedbackX], y=y[b])
        b += 1
        self.feedbackLabel2 = tk.Label(self, text="")
        self.feedbackLabel2.place(x=x[feedbackX], y=y[b])
        b += 1
        self.widgets.append(self.quit)
        self.widgets.append(self.feedbackLabel1)
        self.widgets.append(self.feedbackLabel2)
        self.widgets.append(self.feedbackLabel0)
        self.giveFeedback(-1)
        self.refresh()

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
        if (self.select == 0):
            self.giveFeedback("Reset to make model mode")
        else:
            self.giveFeedback("Reset to use trained model mode")

    # Insert Model helper method
    def load_model(self):
        self.insert_model(self.modelStrVar.get())
        self.refresh()

    def insert_model(self, choice=None):

        self.giveFeedback("Start "+choice+" Insert")
        #print(choice)
        char_idx = create_char_index()
        model = NN_OPTIONS[choice]
        self.cranium.init_model(model(char_idx))
        self.model_inserted = True
        self.model_trained = False
        #print("Model Inserted into Cranium")
        self.giveFeedback("Model Inserted into Cranium")

    def train_model_gui(self):
        #print("Starting Train Model")
        self.giveFeedback("Starting Train Model")
        if (self.pathEntry.get() is "" or self.pathEntry is None):
            self.giveFeedback("No training path, could not train")
            return
        self._build_feed(self.pathEntry.get())
        X, Y = self.feed.get_seq_data()
        data = {'X':X, 'Y':Y}
        for iters in range(self.boundEpoch(self.epochEntry.get())):
            self.cranium.train_model(data, params={'epochs': 1, 'batch_size': 128})
        self.model_trained = True
        self.refresh()
        #print("Model Trained")
        self.giveFeedback("Model Trained")

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
        self.model_trained = False

        for i in range(len(self.widgets)):
            self.widgets[i].destroy()

        self.widgets = []

    def spit_gui(self):
        self.fire = self.cranium.spit(temp=self.boundTemp(self.tempEntry.get()))
        self.outputWindow.insert(tk.END, self.fire)
        self.refresh()
        print(self.fire)

    def save_fire(self):
        None

    def save_model(self):
        None


    def refresh(self):
        for i in range(len(self.widgets)):
            self.widgets[i]["state"] = tk.NORMAL

        if self.select == 0:

            if self.fire == None:
                self.saveFireButton["state"] = tk.DISABLED
            else:
                return

            #Spit widgets
            if not self.model_trained:
                self.spitButton["state"] = tk.DISABLED
                self.tempEntry["state"] = tk.DISABLED
                self.saveFireButton["state"] = tk.DISABLED
            else:
                return

            if not self.model_inserted:
                self.trainButton["state"] = tk.DISABLED
                self.saveModelButton["state"] = tk.DISABLED
                self.pathEntry["state"] = tk.DISABLED
                self.epochEntry["state"] = tk.DISABLED
            else:
                return

            # Load widgets
            if self.modelStrVar.get() is "Choose RNN":
                self.loadButton["state"] == tk.DISABLED

        # For pre-trained model
        else:
            None #change later

    #===================== methods to stop users from being smartasses (and some other stuff)

    def giveFeedback(self, txt):
        if txt == -1:
            self.feedbackLabel0["text"] = self.feedback[0]
            self.feedbackLabel1["text"] = self.feedback[1]
            self.feedbackLabel2["text"] = self.feedback[2]
            return
        self.feedback.append(txt)
        self.feedback.pop(0)
        self.giveFeedback(-1)

    def boundTemp(self, temp):
        try:
            temp = float(temp)
        except ValueError:
            self.giveFeedback("Not a float. Setting temp to 0.5")
            return 0.5

        #temp = float(temp)

        if temp <= 0:
            self.giveFeedback("Float too low, Setting temp to 0.01")
            return 0.01
        elif temp > 1:
            self.giveFeedback("Float too high, Setting temp to 1")
            return 1
        return temp

    def boundEpoch(self, epoch):
        try:
            epoch = int(epoch)
            return epoch
        except ValueError:
            self.giveFeedback("Not an int. Setting epoch to 1")
            return 1


root = tk.Tk()
root.geometry("950x400+300+300")
app = Gui(master=root)
app.mainloop()
