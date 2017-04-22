import tkinter as tk
import csv

class Window:
    def __init__(self, master):
        self.filename=""
        csvfile=tk.Label(root, text="File").grid(row=1, column=0)
        self.bar=tk.Entry(master)
        self.bar.grid(row=1, column=1)
        #Buttons
        y=7
        self.cbutton= tk.Button(root, text="OK", command=self.process_csv)
        y+=1
        self.cbutton.grid(row=10, column=3, sticky = tk.W + tk.E)
        self.bbutton= tk.Button(root, text="Browse", command=self.browsecsv)
        self.bbutton.grid(row=1, column=3)

    def set_text(self,text):
        self.bar.delete(0, tk.END)
        self.bar.insert(0, text)
        return
    def browsecsv(self):
        from tkinter import filedialog

        #withdraw()
        self.filename = filedialog.askopenfilename()
        self.set_text(self.filename)

    def process_csv(self):
        if self.filename:
            with open(self.filename, 'rb') as csvfile:
                logreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                rownum=0

                for row in logreader:
                    NumColumns = len(row)
                    rownum += 1

                Matrix = [[0 for x in tk.xrange(NumColumns)] for x in tk.xrange(rownum)]

root = tk.Tk()
window=Window(root)
root.mainloop()