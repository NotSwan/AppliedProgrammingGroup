from tkinter import *
from tkinter import ttk
from user_classes import *
import menu


def main():
    global master
    global menuFrame
    
    master = Tk()
    master.title("CURSE")
    master.columnconfigure(0, weight=1)
    master.rowconfigure(0, weight=1)

    BGFrameStyle = ttk.Style()
    BGFrameStyle.configure('BG.TFrame', background = "#71b3c7")

    labelStyle = ttk.Style()
    labelStyle.configure('ST.TLabel', foreground="#8052a1", background="#71b3c7")

    menuFrame = LabelFrame(master, text="Welcome to CURSE", foreground="#8052a1", background="#71b3c7")
    menuFrame.grid(column=0,row=0,sticky=(N,W,E,S))

    button1 = ttk.Button(menuFrame, text="Login", command=login_frame)
    button1.grid(padx=100, pady=50)

    master.mainloop()

def login_frame():
    global loginFrame
    global username
    global password
    username = StringVar(master=master, value="haynese")
    password = StringVar(master=master, value="password")

    menuFrame.grid_remove()
    loginFrame = LabelFrame(master, text="Please Login to CURSE", foreground="#8052a1", background="#71b3c7")
    loginFrame.grid(column=0,row=0,sticky=(N,W,E,S))

    label1 = ttk.Label(loginFrame, text="Username: ", style='ST.TLabel')
    label2 = ttk.Label(loginFrame, text="Password: ", style="ST.TLabel")
    label1.grid(column=0,row=0,padx=10,pady=5)
    label2.grid(column=0,row=1,padx=10,pady=5)

    entry1 = ttk.Entry(loginFrame, textvariable=username)
    entry2 = ttk.Entry(loginFrame, textvariable=password,show='*')
    entry1.grid(column=1,row=0,padx=10,pady=5)
    entry2.grid(column=1,row=1,padx=10,pady=5)

    button2 = ttk.Button(loginFrame, text="Login", command=try_login)
    button2.grid(column=2, row=1, padx=10, pady=5)

def try_login():
    global user
    right_password = (db.execute("SELECT password FROM Logins WHERE username = '" + (username.get()) + "'")).fetchone()
    user = menu.login(username.get(), password.get(), right_password[0])
    if user != None:
        main_menu()

def main_menu():
    global mainMenuFrame
    global output
    try:
        output.destroy()
    except:
        pass
    loginFrame.grid_remove()
    mainMenuFrame = LabelFrame(master, text="Main Menu", foreground="#8052a1", background="#71b3c7")
    mainMenuFrame.grid(column=0,row=0,sticky=(N,E,W,S))
    
    welcomeMessage = ttk.Label(mainMenuFrame, text=("Welcome " + user.firstName), font=25,style='ST.TLabel')
    welcomeMessage.grid(column=0,row=0, padx=10, pady=5)

    message0 = ttk.Button(mainMenuFrame, text="Logout", command=logout)
    message1 = ttk.Button(mainMenuFrame, text="List all courses", command=list_all)
    message2 = ttk.Button(mainMenuFrame, text="Search classes")
    message0.grid(column= 1, row=0, padx=10, pady=5)
    message1.grid(column= 0, row=1, padx=10, pady=5, sticky=W)
    message2.grid(column= 0, row=2, padx=10, pady=5, sticky=W)

    if(isinstance(user, Admin)):
        message3 = ttk.Button(mainMenuFrame, text="Add Course")
        message4 = ttk.Button(mainMenuFrame, text="Remove Course(s)")
        message5 = ttk.Button(mainMenuFrame, text="Add User", command=new_user)
        message6 = ttk.Button(mainMenuFrame, text="Link/Unlink Courses")
        message3.grid(column=0, row=3, padx=10, pady=5, sticky=W)
        message4.grid(column=0, row=4, padx=10, pady=5, sticky=W)
        message5.grid(column=0, row=5, padx=10, pady=5, sticky=W)
        message6.grid(column=0, row=6, padx=10, pady=5, sticky=W)

    if(isinstance(user, Student)):
        message3 = ttk.Button(mainMenuFrame, text="Add Course")
        message4 = ttk.Button(mainMenuFrame, text="Remove Course(s)")
        message5 = ttk.Button(mainMenuFrame, text="Print Roster")
        message3.grid(column=0, row=3, padx=10, pady=5, sticky=W)
        message4.grid(column=0, row=4, padx=10, pady=5, sticky=W)
        message5.grid(column=0, row=5, padx=10, pady=5, sticky=W)
    
    if(isinstance(user, Instructor)):
        message3 = ttk.Button(mainMenuFrame, text="Print Schedule")
        message4 = ttk.Button(mainMenuFrame, text="Search Courses")
        message3.grid(column=0, row=3, padx=10, pady=5, sticky=W)
        message4.grid(column=0, row=4, padx=10, pady=5, sticky=W)

def logout():
    mainMenuFrame.grid_remove()
    user = None
    login_frame()

def list_all():
    try:
        output.destroy()
    except:
        pass
    print(user.print_all_courses())
    output = ttk.Label(mainMenuFrame, text=user.print_all_courses(), style='ST.TLabel')
    output.grid(column=1,row=1, rowspan=5)

def new_user():
    mainMenuFrame.grid_remove()
    newCourseFrame = LabelFrame(master, text="Add a New Course", foreground="#8052a1", background="#71b3c7")
    newCourseFrame.grid(column=0, row=0, sticky=(N,E,W,S)) 
    question0 = ttk.Label(newCourseFrame, style='ST.TLabel', text="First Name")
    question1 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Last Name")
    question2 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Account Type")
    question3 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Office(Optional)")
    question4 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Dept(Optional)")
    question5 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Major(Optional)")
    question6 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Hire Year(Optional)")
    question7 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Grad Year(Optional)")
    question0.grid(column=0,row=0,padx=10,pady=5, sticky=W)
    question1.grid(column=0,row=1,padx=10,pady=5, sticky=W)
    question2.grid(column=0,row=2,padx=10,pady=5, sticky=W)
    question3.grid(column=0,row=3,padx=10,pady=5, sticky=W)
    question4.grid(column=0,row=4,padx=10,pady=5, sticky=W)
    question5.grid(column=0,row=5,padx=10,pady=5, sticky=W)
    question6.grid(column=0,row=6,padx=10,pady=5, sticky=W)
    question7.grid(column=0,row=7,padx=10,pady=5, sticky=W)
    
    q0 = StringVar(newCourseFrame, "")
    q1 = StringVar(newCourseFrame, "")
    q2 = StringVar(newCourseFrame, "")
    q3 = StringVar(newCourseFrame, "")
    q4 = StringVar(newCourseFrame, "")
    q5 = StringVar(newCourseFrame, "")
    q6 = StringVar(newCourseFrame, "")
    q7 = StringVar(newCourseFrame, "")

    question0 = ttk.Entry(newCourseFrame, textvariable=q0)
    question1 = ttk.Entry(newCourseFrame, textvariable=q1)
    question2 = ttk.Entry(newCourseFrame, textvariable=q2)
    question3 = ttk.Entry(newCourseFrame, textvariable=q3)
    question4 = ttk.Entry(newCourseFrame, textvariable=q4)
    question5 = ttk.Entry(newCourseFrame, textvariable=q5)
    question6 = ttk.Entry(newCourseFrame, textvariable=q6)
    question7 = ttk.Entry(newCourseFrame, textvariable=q7)
    question0.grid(column=1,row=0,padx=10,pady=5, sticky=W)
    question1.grid(column=1,row=1,padx=10,pady=5, sticky=W)
    question2.grid(column=1,row=2,padx=10,pady=5, sticky=W)
    question3.grid(column=1,row=3,padx=10,pady=5, sticky=W)
    question4.grid(column=1,row=4,padx=10,pady=5, sticky=W)
    question5.grid(column=1,row=5,padx=10,pady=5, sticky=W)
    question6.grid(column=1,row=6,padx=10,pady=5, sticky=W)
    question7.grid(column=1,row=7,padx=10,pady=5, sticky=W)
    
    button1 = ttk.Button(newCourseFrame, text="Return", command=main_menu)
    button2 = ttk.Button(newCourseFrame, text="Add user", command=user.create_new_user(
    q0.get(),   
    q1.get(),
    q2.get(),
    q3.get(),
    q4.get(),
    q5.get(),
    q6.get(),
    q7.get()))

    button1.grid(column=0, row=8, padx=10, pady=5)
    button2.grid(column=1, row=8, padx=10, pady=5)
if __name__ == '__main__':
    main()