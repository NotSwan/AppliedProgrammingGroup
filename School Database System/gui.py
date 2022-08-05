from glob import glob
from tkinter import *
from tkinter import ttk
from user_classes import *
import menu
#######################################################################
# Check List
# All
#   Login - Done
#   Search for courses - Done
# Student
#   Add/Remove Course From Schedule - Done
#   Check Conflicts - Done
#   Print Indiviual Schedule - Done
# Instructor
#   Print Course teaching schedule - Done
#   Print/Search course roster(s) - Done
# Admin
#   Add Courses - Done
#   Remove Courses - Done
#   Add Instructors/Students - Done
#   Link/Unlink instr/students from course - Done
######################################################################
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
    username = StringVar(master=master, value="")
    password = StringVar(master=master, value="")

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
    if (db.execute("SELECT ID FROM Logins WHERE username = '" + username.get() + "'")).fetchone() is None:
        main_menu()
    else:
        db.execute("UPDATE Logins SET password = '" + password.get() + "' WHERE username ='" + username.get() + "'")
        user = menu.login(username.get(), password.get(), password.get())
        main_menu()

def main_menu():
#######################################################
# this is the menu that will branch off into different
# submenus as well as containing some satelitte
# functions that output schedules
#######################################################
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
    message2 = ttk.Button(mainMenuFrame, text="Search classes",command=search_with_params)
    message0.grid(column= 2, row=0, padx=10, pady=5)
    message1.grid(column= 0, row=1, padx=10, pady=5, sticky=W)
    message2.grid(column= 0, row=2, padx=10, pady=5, sticky=W)

    if(isinstance(user, Admin)):
        message3 = ttk.Button(mainMenuFrame, text="Add Course", command= new_course)
        message4 = ttk.Button(mainMenuFrame, text="Remove Course(s)", command=delete_course)
        message5 = ttk.Button(mainMenuFrame, text="Add User", command=new_user)
        message6 = ttk.Button(mainMenuFrame, text="Link/Unlink Courses", command=link_unlink)
        message3.grid(column=0, row=3, padx=10, pady=5, sticky=W)
        message4.grid(column=0, row=4, padx=10, pady=5, sticky=W)
        message5.grid(column=0, row=5, padx=10, pady=5, sticky=W)
        message6.grid(column=0, row=6, padx=10, pady=5, sticky=W)

    if(isinstance(user, Student)):
        message3 = ttk.Button(mainMenuFrame, text="Add/Remove Course", command=student_link)
        message5 = ttk.Button(mainMenuFrame, text="Print Schedule", command=print_schedule)
        message3.grid(column=0, row=5, padx=10, pady=5, sticky=W)
        message5.grid(column=0, row=3, padx=10, pady=5, sticky=W)
    
    if(isinstance(user, Instructor)):
        message3 = ttk.Button(mainMenuFrame, text="Print Schedule", command=print_schedule)
        message4 = ttk.Button(mainMenuFrame, text="Search Courses", command=search_rosters)
        message3.grid(column=0, row=3, padx=10, pady=5, sticky=W)
        message4.grid(column=0, row=4, padx=10, pady=5, sticky=W)

    buttonCmt = ttk.Button(mainMenuFrame, text="Commit", command=db.commit)
    buttonCmt.grid(column=1,row=0,padx=10,pady=5)

def print_schedule():
#######################################################
# this is a dual function for students and instructors
# to see their schedule using the main output label 
# in the mainMenuFrame
#######################################################
    try:
        output.destroy()
    except:
        pass
    if(isinstance(user, Student)):
        output = ttk.Label(mainMenuFrame, text=user.print_my_courses(), style='ST.TLabel')
        output.grid(column=1,row=1, rowspan=5)
    if(isinstance(user, Instructor)):
        output = ttk.Label(mainMenuFrame, text=user.print_course_roaster(), style='ST.TLabel')
        output.grid(column=1,row=1, rowspan=5)

def search_rosters():
#######################################################
# search_rosters moves the user to a frame that 
# prompts the instructor to input a CRN and will
# return the classes list of students
#######################################################       
    def roster_callback():
        temp = user.print_roster(classNum.get())
        out = ttk.Label(frameSR, style='ST.TLabel', text=temp)
        out.grid(column=1,row=1, padx=10, pady=5)
        
    mainMenuFrame.grid_remove()
    frameSR = LabelFrame(master, text="Search Roster", foreground="#8052a1", background="#71b3c7")
    frameSR.grid(column=0,row=0,sticky=(N,E,W,S))
    
    classNum = StringVar(frameSR, "")
    
    lbl = ttk.Label(frameSR, text="CRN: ", style='ST.TLabel')
    lbl.grid(column=0,row=0,padx=10,pady=5)
    
    ent1 = ttk.Entry(frameSR, textvariable=classNum)
    ent1.grid(column=1,row=0,padx=10,pady=5)
    
    button0 = ttk.Button(frameSR, text="Search", command=roster_callback)
    button0.grid(column=2, row=1, padx=10, pady=5)
    btn = ttk.Button(frameSR, text="Return", command=main_menu)
    btn.grid(column=0, row=2, padx=10,pady=5)
        
def link_unlink():
    mainMenuFrame.grid_remove()
    linkFrame = LabelFrame(master, text="Link/Unlink", foreground="#8052a1", background="#71b3c7")
    linkFrame.grid(column=0,row=0,sticky=(N,E,W,S))
    button0 = ttk.Button(linkFrame, text="Student Menu", command=student_link)
    if(isinstance(user,Admin)):
        button1 = ttk.Button(linkFrame, text="Instructor Menu", command=instructor_link)
        button1.grid(column=2, row=0, padx=10,pady=5)
    button2 = ttk.Button(linkFrame, text="Menu", command=main_menu)
    button0.grid(column=0, row=0, padx=10, pady=5)
    button2.grid(column=1, row=1, padx=10,pady=5)

def student_link():
    def add_std_callback():
        if(isinstance(user, Admin)):
            temp = user.enroll_for_student(ID.get(), classID.get())
        elif(isinstance(user, Student)):
            temp = user.enroll(classID.get())
        lbl = ttk.Label(link, text=temp, style='ST.TLabel')
        lbl.grid(column=0,row=3,padx=10,pady=5)

    def rmv_std_callback():
        if(isinstance(user, Admin)):
            temp = user.drop_for_student(ID.get(),classID.get()) 
        elif(isinstance(user, Student)):
            temp = user.drop(classID.get())
        lbl = ttk.Label(link, text=temp, style='ST.TLabel')
        lbl.grid(column=0,row=3,padx=10,pady=5)

    link = LabelFrame(master, text="Student Link/Unlink", foreground="#8052a1", background="#71b3c7")
    link.grid(column=0,row=0,sticky=(N,E,W,S))
    ID = StringVar(link,"")
    classID = StringVar(link, "")
    if(isinstance(user, Admin)):
        lbl = ttk.Label(link, text="Student ID: ", style='ST.TLabel')
        lbl.grid(column=0,row=0,padx=10,pady=5)
        ent1 = ttk.Entry(link, textvariable=ID)
        ent1.grid(column=1,row=0,padx=10,pady=5)
    lbl = ttk.Label(link, text="CRN: ", style='ST.TLabel')
    lbl.grid(column=0,row=1,padx=10,pady=5)

    

    ent2 = ttk.Entry(link, textvariable=classID)
    ent2.grid(column=1,row=1,padx=10,pady=5)

    add = ttk.Button(link, text="Add",command=add_std_callback)
    add.grid(column=2,row=0,padx=10,pady=5, sticky=E)
    rmv = ttk.Button(link, text="Remove",command=rmv_std_callback)
    rmv.grid(column=2,row=1,padx=10,pady=5, sticky=E)

    btn = ttk.Button(link, text="Return", command=link_unlink)
    btn.grid(column=2, row=2, padx=10,pady=5)



def instructor_link():
    global ID
    global classID
    global link
    
    def add_inst_callback():
        user.assign_for_instructor(ID.get(), classID.get())
    def rmv_inst_callback():
        user.remove_for_instructor(ID.get(), classID.get())
        
    link = LabelFrame(master, text="Instructor Link/Unlink", foreground="#8052a1", background="#71b3c7")
    link.grid(column=0,row=0,sticky=(N,E,W,S))

    lbl = ttk.Label(link, text="Instructor ID: ", style='ST.TLabel')
    lbl.grid(column=0,row=0,padx=10,pady=5)
    lbl = ttk.Label(link, text="CRN: ", style='ST.TLabel')
    lbl.grid(column=0,row=1,padx=10,pady=5)

    ID = StringVar(link,"")
    classID = StringVar(link, "")
    ent1 = ttk.Entry(link, textvariable=ID)
    ent1.grid(column=1,row=0,padx=10,pady=5)
    ent2 = ttk.Entry(link, textvariable=classID)
    ent2.grid(column=1,row=1,padx=10,pady=5)

    add = ttk.Button(link, text="Add",command=add_inst_callback)
    add.grid(column=2,row=0,padx=10,pady=5, sticky=E)
    rmv = ttk.Button(link, text="Remove",command=rmv_inst_callback)
    rmv.grid(column=2,row=1,padx=10,pady=5, sticky=E)

    btn = ttk.Button(link, text="Return", command=link_unlink)
    btn.grid(column=2, row=2, padx=10,pady=5)
    

def logout():
#######################################################
# logouts user by removing the previous frame and 
# making user equivalent to None as well as returning
# to the login frame
#######################################################
    mainMenuFrame.grid_remove()
    user = None
    login_frame()

def list_all():
#######################################################
# Since this interfaces directly to the mainMenuFrame
# you must try-except output.destroy then output to 
# the label object in the mainMenuFrame
# could be fixed if relocated but risk error
#######################################################
    try:
        output.destroy()
    except:
        pass
    output = ttk.Label(mainMenuFrame, text=user.print_all_courses(), style='ST.TLabel')
    output.grid(column=1,row=1, rowspan=5)

def search_with_params():
#######################################################
# Single input and buttons to choose what param used
# Takes input and callsback to one of a group of 
# callbacks that will output the handled user function
#######################################################
    def search_with_params_callback_1():
        temp = user.search_courses("CRN", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_2():  
        temp = user.search_courses("title", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_3():  
        temp = user.search_courses("days", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_4():     
        temp = user.search_courses("year", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_5():       
        temp = user.search_courses("credits", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_6():  
        temp = user.search_courses("dept", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    def search_with_params_callback_7():

        temp = user.search_courses("instructor", search.get())
        label0 = ttk.Label(searchFrame, style='ST.TLabel', text=temp)
        label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)

    mainMenuFrame.grid_remove()
    searchFrame = LabelFrame(master, text="Search With Paramaters", foreground="#8052a1", background="#71b3c7")
    searchFrame.grid(column=0, row=0, sticky=(N,E,W,S))
    search = StringVar(searchFrame, "")
    button0 = ttk.Button(searchFrame, text="CRN", command=search_with_params_callback_1)
    button1 = ttk.Button(searchFrame, text="Title", command=search_with_params_callback_2)
    button2 = ttk.Button(searchFrame, text="Days", command=search_with_params_callback_3)
    button3 = ttk.Button(searchFrame, text="Year", command=search_with_params_callback_4)
    button4 = ttk.Button(searchFrame, text="Credits", command=search_with_params_callback_5)
    button5 = ttk.Button(searchFrame, text="Dept", command=search_with_params_callback_6)
    button6 = ttk.Button(searchFrame, text="Instructor", command=search_with_params_callback_7)
    entry0 = ttk.Entry(searchFrame, textvariable=search)
    
    label0 = ttk.Label(searchFrame, style='ST.TLabel', text="")
    
    button0.grid(column=0,row=0,padx=10,pady=5)
    button1.grid(column=0,row=1,padx=10,pady=5)
    button2.grid(column=0,row=2,padx=10,pady=5)
    button3.grid(column=0,row=3,padx=10,pady=5)
    button4.grid(column=0,row=4,padx=10,pady=5)
    button5.grid(column=0,row=5,padx=10,pady=5)
    button6.grid(column=0,row=6,padx=10,pady=5)
    entry0.grid(column=1,row=0,padx=10,pady=5)
    label0.grid(column=1, row=1, padx=10,pady=5, rowspan=3)
    button10 = ttk.Button(searchFrame, text="Return", command=main_menu)
    button10.grid(column=0, row=8, padx=10, pady=5)

def new_user():
#######################################################
# Creates a new user using callbacks to use function
# Handles input for all possible inputs
# Uses cleanInput() to not cause errors with user func
#######################################################
    mainMenuFrame.grid_remove()
    
    def create_user_callback():
        user.create_new_user(cleanInput(q0.get()), cleanInput(q1.get()), cleanInput(q2.get()))
    
    newCourseFrame = LabelFrame(master, text="Add a New Course", foreground="#8052a1", background="#71b3c7")
    newCourseFrame.grid(column=0, row=0, sticky=(N,E,W,S)) 
    question0 = ttk.Label(newCourseFrame, style='ST.TLabel', text="First Name")
    question1 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Last Name")
    question2 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Account Type")
    question3 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Office(Admin)")
    question4 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Dept(Instructors)")
    question5 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Major(Students)")
    question6 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Hire Year(Instructors)")
    question7 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Grad Year(Students)")
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
    button2 = ttk.Button(newCourseFrame, text="Add user", command=create_user_callback)

    button1.grid(column=0, row=8, padx=10, pady=5)
    button2.grid(column=1, row=8, padx=10, pady=5)

def new_course():
#######################################################
# Creates a new course utilizing a callback function
# Callback handles the commands with inputs
# User input for all possible values for courses
#######################################################
    mainMenuFrame.grid_remove()
    
    def create_course_callback():
        user.create_new_course(cleanInput(q0.get()), cleanInput(q1.get()), cleanInput(q2.get()), cleanInput(q3.get()), cleanInput(q4.get()), cleanInput(q5.get()), cleanInput(q6.get()))

    newCourseFrame = LabelFrame(master, text="Add a New Course", foreground="#8052a1", background="#71b3c7")
    newCourseFrame.grid(column=0, row=0, sticky=(N,E,W,S)) 
    question0 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Title")
    question1 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Start Time")
    question2 = ttk.Label(newCourseFrame, style='ST.TLabel', text="End Time")
    question3 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Days")
    question4 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Year")
    question5 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Credits")
    question6 = ttk.Label(newCourseFrame, style='ST.TLabel', text="Dept")


    question0.grid(column=0,row=0,padx=10,pady=5, sticky=W)
    question1.grid(column=0,row=1,padx=10,pady=5, sticky=W)
    question2.grid(column=0,row=2,padx=10,pady=5, sticky=W)
    question3.grid(column=0,row=3,padx=10,pady=5, sticky=W)
    question4.grid(column=0,row=4,padx=10,pady=5, sticky=W)
    question5.grid(column=0,row=5,padx=10,pady=5, sticky=W)
    question6.grid(column=0,row=6,padx=10,pady=5, sticky=W)

    q0 = StringVar(newCourseFrame, "")
    q1 = StringVar(newCourseFrame, "")
    q2 = StringVar(newCourseFrame, "")
    q3 = StringVar(newCourseFrame, "")
    q4 = StringVar(newCourseFrame, "")
    q5 = StringVar(newCourseFrame, "")
    q6 = StringVar(newCourseFrame, "")

    question0 = ttk.Entry(newCourseFrame, textvariable=q0)
    question1 = ttk.Entry(newCourseFrame, textvariable=q1)
    question2 = ttk.Entry(newCourseFrame, textvariable=q2)
    question3 = ttk.Entry(newCourseFrame, textvariable=q3)
    question4 = ttk.Entry(newCourseFrame, textvariable=q4)
    question5 = ttk.Entry(newCourseFrame, textvariable=q5)
    question6 = ttk.Entry(newCourseFrame, textvariable=q6)

    question0.grid(column=1,row=0,padx=10,pady=5, sticky=W)
    question1.grid(column=1,row=1,padx=10,pady=5, sticky=W)
    question2.grid(column=1,row=2,padx=10,pady=5, sticky=W)
    question3.grid(column=1,row=3,padx=10,pady=5, sticky=W)
    question4.grid(column=1,row=4,padx=10,pady=5, sticky=W)
    question5.grid(column=1,row=5,padx=10,pady=5, sticky=W)
    question6.grid(column=1,row=6,padx=10,pady=5, sticky=W)

    
    button1 = ttk.Button(newCourseFrame, text="Return", command=main_menu)
    button2 = ttk.Button(newCourseFrame, text="Add Course", command=create_course_callback)

    button1.grid(column=0, row=8, padx=10, pady=5)
    button2.grid(column=1, row=8, padx=10, pady=5)

def cleanInput(input):
#######################################################
# Used to make empty strings pass None
# Mainly used in creating users due to many possible 
# Values being left empty
#######################################################
    if (input == ""):
        return None
    else:
        return input

def delete_course():
#######################################################
# Deletes course from system
# Uses a callback to handle input from user
# Takes a single CRN num as input
#######################################################
    def delete_course_callback():
        user.remove_entry('Courses', int(crn.get()))
        
    mainMenuFrame.grid_remove()
    newCourseFrame = LabelFrame(master, text="Delete Course", foreground="#8052a1", background="#71b3c7")
    newCourseFrame.grid(column=0, row=0, sticky=(N,E,W,S)) 
    crn = StringVar(newCourseFrame, "")
    label = ttk.Label(newCourseFrame, style='ST.TLabel', text="CRN")
    label.grid(column=0,row=0,padx=10,pady=5, sticky=W)
    question0 = ttk.Entry(newCourseFrame, textvariable=crn)
    question0.grid(column=1,row=0,padx=10,pady=5, sticky=W)
    button1 = ttk.Button(newCourseFrame, text="Return", command=main_menu)
    button2 = ttk.Button(newCourseFrame, text="Delete", command=delete_course_callback)
    button1.grid(column=0, row=8, padx=10, pady=5)
    button2.grid(column=1, row=8, padx=10, pady=5)

if __name__ == '__main__':
    main()