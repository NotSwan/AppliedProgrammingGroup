import tkinter as tk
from tkinter import ttk
from tkinter import N,W,S,E


def menu():
    global root
    global mainframe
    global mainStyle
    root = tk.Tk()
    root.title("CURSE")

    mainStyle = ttk.Style()
    mainStyle.configure('BG.TFrame', background = "#71b3c7")
    labelStyle = ttk.Style()
    labelStyle.configure('BG.TLabel', foreground="#8052a1", background="#71b3c7")
    mainframe = ttk.Frame(root, width=800, height=600, style='BG.TFrame')
    mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame1 = ttk.LabelFrame(mainframe, text="Welcome to CURSE", style='BG.TLabel').grid(column=1, row=0,padx=100,pady=50)
    ttk.Button(frame1, command=login_menu, text="Login").grid(column=1,row=1)
    
    
    root.mainloop()


def login_menu():
    username = StringVar()
    password = StringVar()
    ttk.Label(mainframe, text="Username: ").grid(column=0,row=0,padx=10,pady=5)
    ttk.Label(mainframe, text="Password: ", foreground="#8052a1", background="#71b3c7").grid(column=1,row=0,padx=10,pady=5)
    ttk.Entry(mainframe, username).grid(column=1,row=0,padx=10,pady=5)
    ttk.Entry(mainframe, password).grid(column=1,row=1, padx=10,pady=5)


if __name__ == '__main__':
    menu()