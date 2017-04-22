import tkinter as tk
import pyperclip as py
root = tk.Tk()
frame = tk.Frame(root)
#frame.pack()


def clickAbout():
    toplevel = tk.Toplevel()
    label1 = tk.Label(toplevel, text="About_Text", height=0, width=100)
    label1.pack()
    label2 = tk.Label(toplevel, text="Disclaimer", height=0, width=100)
    label2.pack()

def generateText(cur_frame):
    cur_frame.insert(tk.END, "Hello.....")
    cur_frame.pack(side = tk.BOTTOM)
def editTop():
    toplevel = tk.Toplevel()
    toplevel.focus_force()
    label3 = tk.Label(toplevel,text="About_Text", height=0, width = 100)
    label3.pack()
    generateText(tk.Text(toplevel))
def copy():
    py.copy('The text to be copied to the clipboard.')
    print(py.paste())


bottomframe = tk.Frame(root)
bottomframe.pack( side = tk.BOTTOM )

redbutton = tk.Button(frame, text="Red", fg="red", command=clickAbout)
redbutton.pack( side = tk.LEFT)

brownbutton = tk.Button(frame, text="Brown", fg="brown", command=editTop)
brownbutton.pack( side = tk.LEFT )

bluebutton = tk.Button(frame, text="Blue", fg="blue",command=lambda:generateText(tk.Text(frame)))
bluebutton.pack( side = tk.LEFT )


blackbutton = tk.Button(bottomframe, text="Black", fg="black",command=copy)
blackbutton.pack( side = tk.BOTTOM)

frame.pack()
root.mainloop()
