import sqlite3 as sql
import Assignment1_TylerSwan

#https://wentworth.brightspace.com/d2l/le/content/24962/viewContent/292676/View
#https://wentworth.brightspace.com/d2l/le/content/24962/viewContent/297072/View

global userTypes
userTypes = {"1":"Student","2":}


# Contributors: Tyler Swan
# Variables:
# Use:
#
#
def main():
    mainMenu()

# Contributors: Tyler Swan
# Variables:
# Use:
#
#
def mainMenu():
    print("Welcome to The School Managment System")
    print("Please log on to continue")
    print("What are you logging in as today\n \
            1. Student \n \
            2. Instructor\n \
            3. Admin")
    userType = "0"
    while (userType < 1 or userType > 3):
        userType = input("User type: ")
    user = input("\nEnter username: ")
    passW = "_"
    exist = check_user(user)
    if(exist):
        passW = input("\nEnter password: ")
    else:
        print("Username does not exist")
        logIO(userType, user, passW, exist)

# Contributors: 
# Variables:
# Use:
#
#
def addRemoveClass():
    pass

# Contributors: 
# Variables:
# Use:
#
#
def printInstRoster():
    pass

# Contributors: 
# Variables:
# Use:
#
#
def addRemoveCourseAdmin():
    pass

# Contributors: Tyler Swan
# Variables: 
#   (boolean) logIn: True = log IN , False = log OUT
#
# Use:
#
#
def logIO(type, user, passW, logIn):
    if(logIn):
        try:
            db = sql.connect("Assignment5/userList.db")
        except:
            pass
        db.execute("SELECT from ADMIN where email = ",user)
    else:
        print("Exitting sys")


# Contributors: 
# Variables:
# Use:
#
#
def check_user(usr):
    try:
        db = sql.connect("Assignment5/userList.db")
    except:
        pass
    # try:
    #     db.execute("ALTER TABLE ADMIN ADD COLUMN passWord")
    # except:
    #    pass
    # try:
    #     db.execute("ALTER TABLE INSTRUCTOR ADD COLUMN passWord")
    # except:
    #     pass
    # try:
    #     db.execute("ALTER TABLE STUDENT ADD COLUMN passWord")
    # except:
    #     pass
    cursor = db.execute("SELECT email from ADMIN")
    exist = False
    for email in cursor:
        print(email[0])
        if(not exist):
            exist = (email[0] == usr)

    cursor = db.execute("SELECT email from STUDENT")
    for email in cursor:
        print(email[0])
        if(not exist):
            exist = (email[0] == usr)

    cursor = db.execute("SELECT email from INSTRUCTOR")
    for email in cursor:
        print(email[0])
        if(not exist):
            exist = (email[0] == usr)
    return exist
    db.close()


# Contributors: 
# Variables:
# Use:
#
#
def search():
    pass

# Contributors: 
# Variables:
# Use:
#
#
def editClass():
    pass

if __name__ == '__main__':
    main()
