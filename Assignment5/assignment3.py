import sqlite3 as sql
##########
#Attributes:
#Student – ID, first name, last name, expected graduation year, major, email.
#Instructor – ID, first name, last name, title, year of hire, department, email.
#Admin – ID, first name, last name, title, office, email.
#Course – CRN, Title, department, time, day(s) of the week, semester, year, credits.
#
#There are 10 students, 6 instructors, and 2 administrators currently in the database file.
#You need to add 2 students (you choose), remove 1 instructor (you choose), and update 1 administrator (update Vera
#Rubin’s title to “Vice-President”).
#
#You must also populate the course list with 5 courses. Once populated, query the database for various attributes as a
#general test, using your C++ or python code.
#
#For each course you create, you should match it to an instructor. So, you will need to query each course for the
#department and then query the result to find matching (or flag no matching) instructor. The final print out should list
#which instructors can teach which course.
#########

#Initialization with the db
try:
    db = sql.connect("Assignment3/assignment3.db")
    #Student changes
    db.execute("INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (10011, 'Jeff', 'Bezos', '2043', 'BSBM', 'bezosj')")
    db.execute("INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (10012, 'Elon', 'Musk', '2064', 'BSCO', 'muske')")
    #Deleting instructor
    db.execute("DELETE from INSTRUCTOR where ID = 20002;")
    #Updating admin title
    db.execute("UPDATE ADMIN set TITLE = 'Vice-President' where ID = 30002")
    #Class Table 
    db.execute('''CREATE TABLE COURSE
            (CRN INT PRIMARY KEY   NOT NULL,
            TITLE          TEXT    NOT NULL,
            DEPARTMENT     TEXT    NOT NULL,
            TIME           TEXT    NOT NULL,
            DAYS           TEXT    NOT NULL,
            SEMESTER       TEXT    NOT NULL,
            YEAR           INT     NOT NULL,
            CREDITS        INT     NOT NULL);''')

    db.execute("INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (40001, 'Circuits', 'BSEE', '8-9:20am', 'MF', 'Summer', 2022, 3)")
    db.execute("INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (40002, 'Intro to AS', 'BSAS', '5-6:20pm', 'MWF', 'Summer', 2022, 4)")
    db.execute("INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (40003, 'Operating Systems', 'BSCO', '10-11:50am', 'TR', 'Summer', 2022, 3)")
    db.execute("INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (40004, 'Intro to OS', 'BCOS', '12-1:50pm', 'WF', 'Summer', 2022, 4)")
    db.execute("INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (40005, 'Thermodynamics', 'BSME', '1-2:30pm', 'MR', 'Summer', 2022, 3)")

    #Closing of db
    db.commit()
except sql.IntegrityError:
    print("Already populated!\n")

cursorCourses = db.execute( "SELECT title, department from COURSE")
x = list()
for crs in cursorCourses:
    found = False
    print("Seaching for instructors for: ", crs[0]) 
    cursorTeachers = db.execute("SELECT name, surname, dept from INSTRUCTOR") 
    for ins in cursorTeachers:
        if(crs[1] == ins[2] and not found):
            print("Found match: ", ins[0], ins[1])
            x.append((crs[0], ins[0] + ins[1]))
            found = True
    if(not found):
        print("No match found!")
        x.append((crs[0],"NULL"))

print(x)
db.close()