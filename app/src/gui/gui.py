import tkinter as tk
import tensorflow as tf
from tkinter import filedialog

import os.path
from paths import *

from app.src.core.cranium import Cranium
from app.src.core.models.experimental_rnn_configs import *
from app.src.file.song_feed import SongFeed

from app.src.domain.default_char_index import *


NN_OPTIONS = {"Hot Dog RNN":HotDogRnn, "Jumbo Dog RNN":JumboDogRnn, "Hamburger RNN":HamburgerRnn,
              "Pancake RNN":PancakeRnn, "Pizza Dough RNN":PizzaDoughRnn, "Little RNN":LittleRnn}

class Gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Raptimus Prime")
        self.pack(fill=tk.BOTH, expand=1)
        self.select = 0
        self.cranium = Cranium()

        #Lyrics Feed
        self.feed = None
        self.startVar = tk.IntVar()
        self.modelStrVar = tk.StringVar()
        self.trainPath = None
        self.fileDialogPath = None

        #Filters
        self.langFilterVar = tk.IntVar()
        self.engFilterVar = tk.IntVar()
        self.rhymeFilterVar = tk.IntVar()
        self.formatFilterVar = tk.IntVar()

        #variables for what's loaded
        self.model_inserted = False
        self.model_trained = False
        self.fire = None

        self.aPretrainModel = tk.StringVar()
        self.pretrainModels = []

        #This array is for any widget that doesn't have a fixed value
        self.widgets = []
        self.feedback = ["", "", "", "", ""]
        self.create_widgets()
        self.giveFeedback("Welcome to R-Prime")

    def create_widgets(self, initStart=True):
        #Set up
        x = [20]
        y = [10]

        self.G = x
        self.H = y

        for i in range(0, 35):
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
            self.createPreTrainedModelWidgets(x, y, b)

    #Create Initial Widgets that are never deleted and re-created
    def createInitWidgets(self, x, y):
        b = 0

        self.startRadioB1 = tk.Radiobutton(self, text="Make model", variable=self.startVar, value=0,
                                           command=self.changeMode)
        self.startRadioB1.place(x=x[0], y=y[b])

        self.startRadioB2 = tk.Radiobutton(self, text="Use Pre-trained Model", variable=self.startVar, value=1,
                                           command=self.changeMode)
        self.startRadioB2.place(x=x[1], y=y[b])

        self.outputWindow = tk.Text(self, width=55, height=20, wrap=tk.WORD)
        self.outputWindow.place(x=x[4], y=y[b + 1])

    def createPreTrainedModelWidgets(self, x, y, b):
        b+=1

        self.modelLabelPT = tk.Label(self, text="Select RNN:")
        self.modelLabelPT.place(x=x[0], y=y[b])

        self.loadButton2 = tk.Button(self, text="Load", command=self.load_trained_model, width=9)
        self.loadButton2.place(x=x[2], y=y[b])

        # HAVE PRE TRAINED MODELS HERE!!!
        # TODO fix this, the app shouldn't error out if there are no pre trained models
        self.get_trained_models()
        if len(self.pretrainModels) > 0:
            self.aPretrainModel.set(self.pretrainModels[0])
            self.pretrainOptions = tk.OptionMenu(self, self.aPretrainModel, *self.pretrainModels)
        else:
            self.pretrainOptions = tk.Label(self, text="No Models Available")

        self.pretrainOptions.place(x=x[1]-10, y=y[b])
        b += 1

        self.widgets.append(self.modelLabelPT)
        self.widgets.append(self.loadButton2)
        self.widgets.append(self.pretrainOptions)
        self.createSpitWidgets(x, y, b)

    def createModelSelection(self, x, y, b):
        self.modelStrVar.set("Hot Dog RNN")
        self.optionmenu = tk.OptionMenu(self, self.modelStrVar, *NN_OPTIONS.keys())
        #self.optionmenu["command"] = self.refresh
        self.optionmenu.place(x=x[1]-10,y=y[b]-2)

        self.modelLabel = tk.Label(self, text="Select RNN:")
        self.modelLabel.place(x=x[0], y=y[b])
        #b+=1
        self.loadButton = tk.Button(self, text="Load", command=self.load_model, width=9)
        self.loadButton.place(x=x[2], y=y[b])
        b+=1

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

        #FILE DIALOG
        self.fdButton = tk.Button(self, text="Choose Folder", command=self.fileDialogOpen)
        self.fdButton.place(x=x[1], y=y[b])

        self.pathEntry = tk.Entry(self, width=30)
        self.pathEntry.insert(0, "Choose Path")
        self.pathEntry.place(x=x[2], y=y[b])
        b+= 1

        #Append and continue
        self.widgets.append(self.pathEntry)
        self.widgets.append(self.fdButton)
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

        self.seqLenLabel = tk.Label(self, text="Seq Len:")
        self.seqLenLabel.place(x=x[1], y=y[b])
        self.seqLenEntry = tk.Entry(self, width=6)
        self.seqLenEntry.place(x=x[2], y=y[b])
        b += 1
        self.saveFireButton = tk.Button(self, text="Save Spit", command=self.save_fire, width=9)
        self.saveFireButton.place(x=x[0], y=y[b])
        b += 1

        self.langCheckBox = tk.Checkbutton(self, text = "Remove Cursing", variable = self.langFilterVar, \
                         onvalue = 1, offvalue = 0)
        self.langCheckBox.place(x=x[3], y=y[b])
        self.engCheckBox = tk.Checkbutton(self, text = "English", variable = self.engFilterVar, \
                         onvalue = 1, offvalue = 0)
        self.engCheckBox.place(x=x[2], y=y[b])
        self.rhymeFilterBox = tk.Checkbutton(self, text = "Rhyme", variable = self.rhymeFilterVar,\
                                             onvalue = 1, offvalue = 0)
        self.rhymeFilterBox.place(x=x[1],y=y[b])
        b+=1

        self.formatFilterBox = tk.Checkbutton(self, text="Format", variable=self.formatFilterVar, \
                                             onvalue=1, offvalue=0)
        self.formatFilterBox.place(x=x[1], y=y[b])
        b += 1

        self.widgets.append(self.seqLenEntry)
        self.widgets.append(self.seqLenLabel)
        self.widgets.append(self.formatFilterBox)
        self.widgets.append(self.rhymeFilterBox)
        self.widgets.append(self.langCheckBox)
        self.widgets.append(self.engCheckBox)
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
        self.feedbackLabel3 = tk.Label(self, text="")
        self.feedbackLabel3.place(x=x[feedbackX], y=y[b])
        b += 1
        self.feedbackLabel4 = tk.Label(self, text="")
        self.feedbackLabel4.place(x=x[feedbackX], y=y[b])

        self.widgets.append(self.quit)
        self.widgets.append(self.feedbackLabel1)
        self.widgets.append(self.feedbackLabel2)
        self.widgets.append(self.feedbackLabel0)
        self.widgets.append(self.feedbackLabel4)
        self.widgets.append(self.feedbackLabel3)
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
        tf.reset_default_graph()
        self.insert_model(self.modelStrVar.get())
        self.refresh()

    def insert_model(self, choice=None):

        self.giveFeedback("Start "+choice+" Insert")
        char_idx = create_char_index()
        model = NN_OPTIONS[choice]
        self.cranium.init_model(model(char_idx))
        self.model_inserted = True
        self.model_trained = False
        self.giveFeedback("Model Inserted into Cranium")

    def fileDialogOpen(self):
        self.fileDialogPath = filedialog.askdirectory()
        self.pathEntrySetText(self.fileDialogPath)
        self.giveFeedback(self.fileDialogPath)

    def pathEntrySetText(self, text):
        self.pathEntry.delete(0,tk.END)
        self.pathEntry.insert(0,text)

    def train_model_gui(self):
        self.giveFeedback("Starting Train Model")
        if (self.pathEntry.get() is "" or self.pathEntry.get() is "Choose Path" or self.fileDialogPath is None):
            self.giveFeedback("No training path, could not train")
            return
        self._build_feed(self.pathEntry.get())
        X, Y = self.feed.get_seq_data()
        data = {'X':X, 'Y':Y}
        for iters in range(self.boundEpoch(self.epochEntry.get())):
            self.cranium.train_model(data, params={'epochs': 1, 'batch_size': 128})
        self.model_trained = True
        self.refresh()
        self.giveFeedback("Model Trained")

    # Helper Method for train_model
    def _build_feed(self, a_data_dir):
        self.feed = SongFeed.from_lyrics_directory(self.fileDialogPath)

    # Clears widgets to set them up again
    def reset(self, mode=0):
        tf.reset_default_graph()
        self.cranium = Cranium()
        self.feed = None
        self.fire = None
        self.model_inserted = False
        self.model_trained = False

        for i in range(len(self.widgets)):
            self.widgets[i].destroy()

        self.widgets = []

    def spit_gui(self):
        self.giveFeedback("About to spit fire")
        seed = None
        if self.feed:
            try:
                seed = self.feed.seeds[0]
            except Exception:
                pass

        self.fire = self.cranium.spit(temp=self.boundTemp(self.tempEntry.get()), seed=seed,
                format_filter = self.formatFilterVar.get(), language_filter = self.langFilterVar.get(),
                english_filter = self.engFilterVar.get(), rhyme_filter = self.rhymeFilterVar.get(),
                seq_len=self.boundSeqLen(self.seqLenEntry.get()))
        self.outputWindow.config(state="normal")
        self.outputWindow.delete("1.0", tk.END)
        self.outputWindow.insert(tk.END, self.fire)
        self.outputWindow.config(state="disabled")
        self.refresh()
        print(self.fire)


    def save_fire(self):
        self.giveFeedback("Saving Output")
        fileExists = True
        spitSaveNum = 1

        output_path = os.path.join(DATA_DIR, "spit-output\\")
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        while(fileExists):
            out_file = os.path.join(output_path, "output"+str(spitSaveNum)+".txt")
            if not os.path.isfile(out_file):
                with open(out_file,"w") as fo:
                    fo.write(self.fire)
                    fileExists = False
            spitSaveNum+=1

        self.giveFeedback("Output Saved")

    def save_model(self):
        self.giveFeedback("Saving Model")
        modelSaveNum = 1
        pathExists = True
        output_path = None

        output_dir = os.path.join(DATA_DIR, "nn-training-output\\")
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        while(pathExists):
            output_path = os.path.join(DATA_DIR, "nn-training-output\\",
                                       self.modelStrVar.get()+"-"+str(modelSaveNum)+"\\")
            if not os.path.isdir(output_path):
                os.mkdir(output_path)
                pathExists = False
            modelSaveNum+=1

        self.giveFeedback("Saving model to: "+self.modelStrVar.get()+"-"+str(modelSaveNum-1))
        self.cranium.save_state(output_path)
        self.giveFeedback("Model Saved")

    #LOAD PRE TRAINED MODEL
    def load_trained_model(self, nn_dir=None):
        tf.reset_default_graph()
#        self.cranium = Cranium()
        nn_dir = self.aPretrainModel.get()
        self.giveFeedback(nn_dir)
        pretrain_path = os.path.join(DATA_DIR, "pre-trained-models\\", nn_dir)
        trained_path = os.path.join(DATA_DIR, "nn-training-output\\", nn_dir)

        if os.path.isdir(pretrain_path):
            cp_path=os.path.join(pretrain_path)
            self.giveFeedback("pretrain path")
            self.cranium.load_state(cp_path)

        elif os.path.isdir(trained_path):
            cp_path = os.path.join(trained_path)
            self.giveFeedback("trained path")
            self.cranium.load_state(cp_path)

        #else:
            #print("something went wrong")
        self.model_trained = True

    def get_trained_models(self):
        pretrain_path = os.path.join(DATA_DIR,"pre-trained-models\\")
        trained_path = os.path.join(DATA_DIR,"nn-training-output\\")
        if not os.path.isdir(pretrain_path):
            os.mkdir(pretrain_path)
        if not os.path.isdir(trained_path):
            os.mkdir(trained_path)

        self.pretrainModels = os.listdir(pretrain_path)
        for dir in os.listdir(trained_path):
            self.pretrainModels.append(dir)

    def refresh(self):
        for i in range(len(self.widgets)):
            self.widgets[i]["state"] = tk.NORMAL

        self.outputWindow["state"] = tk.DISABLED
        if self.select == 0:

            if self.fire == None:
                self.saveFireButton["state"] = tk.DISABLED
            elif self.model_trained:
                return

            #Spit widgets
            if not self.model_trained:
                self.spitButton["state"] = tk.DISABLED
                self.tempEntry["state"] = tk.DISABLED
                self.saveModelButton["state"] = tk.DISABLED
                if self.fire == None:
                    self.saveFireButton["state"] = tk.DISABLED
            else:
                return

            if not self.model_inserted:
                self.trainButton["state"] = tk.DISABLED
                self.pathEntry["state"] = tk.DISABLED
                self.epochEntry["state"] = tk.DISABLED
                self.fdButton["state"] = tk.DISABLED
            else:
                return

            # Load widgets
            if self.modelStrVar.get() is "Choose RNN":
                self.loadButton["state"] == tk.DISABLED

        # For pre-trained model
        elif self.select == 1:

            if not len(self.pretrainModels) > 0:
                self.loadButton2["state"] = tk.DISABLED

            if self.fire == None:
                self.saveFireButton["state"] = tk.DISABLED
            elif self.model_trained:
                return

            if not self.model_trained:
                self.spitButton["state"] = tk.DISABLED
                self.tempEntry["state"] = tk.DISABLED
                if self.fire == None:
                    self.saveFireButton["state"] = tk.DISABLED
            else:
                return

    #===================== methods to stop users from being smartasses (and some other stuff)

    def giveFeedback(self, txt):
        if txt == -1:
            self.feedbackLabel0["text"] = self.feedback[0]
            self.feedbackLabel1["text"] = self.feedback[1]
            self.feedbackLabel2["text"] = self.feedback[2]
            self.feedbackLabel3["text"] = self.feedback[3]
            self.feedbackLabel4["text"] = self.feedback[4]
            return
        print(txt)
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
        except ValueError:
            self.giveFeedback("Not an int. Setting epoch to 1")
            return 1

        if epoch < 1:
            self.giveFeedback("Epoch less than 1. Setting epoch to 1")
            return 1
        else:
            return epoch

    def boundSeqLen(self, seqLen):
        try:
            seqLen = int(seqLen)
        except ValueError:
            self.giveFeedback("Not an int. Setting seqLen to 200")
            return 200

        if seqLen < 1:
            self.giveFeedback("SeqLen less than 1. Setting epoch to 200")
            return 200
        else:
            return seqLen

root = tk.Tk()
root.geometry("950x500+500+300")
app = Gui(master=root)

def main():
    app.mainloop()

if __name__ == '__main__':
    main()
