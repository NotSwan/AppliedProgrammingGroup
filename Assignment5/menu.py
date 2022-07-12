import sqlite3 as sql
import Assignment1_TylerSwan
# Contributors: Tyler Swan
# Variables:
# Use:
#
#
def main():
    try:
        sql.connect("Assignment5/userList.db")
    except:
        pass
    mainMenu()

# Contributors: Tyler Swan
# Variables:
# Use:
#
#
def mainMenu():
    print("Welcome to The School Managment System")
    print("Please log on to continue")
    logIO(True)

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
# Use:
#
#
def logIO(logIn):
    if logIn:
        user = input("\nEnter username: ")
        passW = input("\nEnter password: ")
        print(user + " " + passW)

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