import tkinter as tk
import string
window = tk.Tk()

window.configure(background="#000000")

window.title("Welcome")
background_image = tk.PhotoImage(file="C:\\Users\\blake\\Desktop\\Pictures\\download.gif")
lblBackground = tk.Label(window,image=background_image)
lblBackground.place(x=0, y=0, relwidth=1, relheight=1)
lblBackground.image=background_image
#lblBackground.pack()
#window.wm_iconbitmap('Icon.ico')

#photo = tk.PhotoImage(file="title.gif")
#w = tk.Label(window, image=photo)
#w.pack()
status = False
def check_status():
    global status
    return status

def Login():
    if check_status() == True:
        print ("Successfully Logged In")
    else:
        print("Please fill out your Username and Password")

def update_status():
    global status
    global entUsername
    print (entUsername.get())
    if status == True:
        status = False
    else:
        status = True

lblInst = tk.Label(window,text="Please login to continue",
                   fg="#e63900",bg="#000000",font=("System",16))
lblInst.pack()

lblUsername = tk.Label(window, text="Username:", fg="#e63900",bg="#000000",
                       font=("Fixedsys",12))
entUsername = tk.Entry(window,bg="#595959")
lblUsername.pack()
entUsername.pack()

lblPassword = tk.Label(window,text="Password:",fg="#e63900",bg="#000000",
                       font=("Fixedsys",12))
entPassword = tk.Entry(window,bg="#595959")

lblPassword.pack()
entPassword.pack()

btn = tk.Button(window,text="Login",fg="#000000",bg="#e63900",
                font=("System",10),relief=tk.RAISED,cursor="box_spiral",command=Login)
btn2 = tk.Button(window,text="Test",command=update_status)
btn.pack()
btn2.pack()

window.mainloop()
