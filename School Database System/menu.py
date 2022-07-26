from user_classes import *


def login_menu():
    print("Enter username:")
    username = input(">").lower()
    if username == "/x":
        return None

    if (db.execute("SELECT ID FROM Logins WHERE username = '" + username + "'")).fetchone() is None:
        print("User does not exist")
        print("Enter /x to return to exit")
        return login_menu()

    password = (db.execute("SELECT password FROM Logins WHERE username = '" + username + "'")).fetchone()[0]
    print(str(password))  # printing the password is definitely a feature we should remove before launch :P

    if password is None:
        print("New User Detected")

    while password is None:
        print("Set password:")
        new_pass1 = input(">")
        print("Confirm password:")
        new_pass2 = input(">")
        if new_pass1 == new_pass2:
            password = new_pass1
            db.execute("UPDATE Logins SET password = '" + password + "' WHERE username ='" + username + "'")
            print("Password set successfully")
            return login_menu()
        else:
            print("Passwords must match")

    print("Enter your password")
    entered_pass = input(">")
    return login(username, password, entered_pass)


def login(username, password, entered_pass):
    if entered_pass == str(password):
        ID = str((db.execute("SELECT ID FROM Logins WHERE username = '" + username + "'")).fetchone()[0])
        accountType = str(
            (db.execute("SELECT accountType FROM Logins WHERE username = '" + username + "'")).fetchone()[0])

        if accountType == "Admin":
            user_info = (db.execute("SELECT * FROM Admin WHERE ID = '" + ID + "'")).fetchmany()[0]
            user = Admin(user_info[1], user_info[2], ID)
            if user_info[4] is not None:
                user.set_office(user_info[4])

        if accountType == "Instructor":
            user_info = (db.execute("SELECT * FROM Instructors WHERE ID = '" + ID + "'")).fetchmany()[0]
            user = Instructor(user_info[1], user_info[2], ID)
            if user_info[4] is not None:
                user.set_dept(user_info[4])

            if user_info[5] is not None:
                user.set_hireYear(user_info[5])

        if accountType == "Student":
            user_info = (db.execute("SELECT * FROM Students WHERE ID = '" + ID + "'")).fetchmany()[0]
            user = Student(user_info[1], user_info[2], ID)
            if user_info[4] is not None:
                user.set_gradYear(user_info[4])

            if user_info[5] is not None:
                user.set_major(user_info[5])

        return user
    print("Exiting...")
    return None

def menu_return(current_user):
    print("enter anything to return")
    input()
    return menu(current_user)


def menu(current_user):
    print("What would you like to do?")
    print("==========================")
    print("view - view all courses")
    print("search - search courses based on parameter")

    if current_user.accountType == "Student":
        print("enroll - add a course to your roster")
        print("drop - drop a course from your roster")
        print("roaster - view the classes you are currently enrolled in")

    if current_user.accountType == "Instructor":
        print("assign - assign self to course")
        print("remove - remove self from course")
        print("roaster - view the classes you are currently teaching")

    if current_user.accountType == "Admin":
        print("create_user - create a new user")
        print("delete_user - delete a user")
        # these will be needed eventually but not for lab 5
        # print("create_course - create a new course")
        # print("delete_course - delete a course")
        # print("enroll_student - enroll a student in a course")
        # print("drop_student - drop a course from a student's roaster")
        # print("search_table - search any table")

    print("logout - exit the system")

    command = input(">")

    # prepare yourself for a gigantic if...elif...elif... statement
    # is there a better way to do this? Probably!

    # user functions

    if command == "view":  # view all courses
        current_user.print_all_courses()
        menu_return(current_user)

    elif command == "search":  # search courses
        print("What field do you want to search by? (CRN, title, days, year, credits, dept, instructor)")
        field = input(">")
        print("Enter search term")
        search = input(">")
        current_user.search_courses(field, search)
        menu_return(current_user)

    elif command == "logout":  # logout from system
        print("Logging out...")
        return main()

    # student functions

    elif current_user.accountType == "Student" and command == "enroll":
        # enroll in a course
        print("Enter the CRN of the course you would like to enroll in")
        CRN = input(">")
        current_user.enroll(CRN)

    elif current_user.accountType == "Student" and command == "drop":  # drop from a course
        print("Enter the CRN of the course you would like to drop")
        CRN = input(">")
        current_user.drop(CRN)

    elif current_user.accountType == "Student" and command == "roaster":
        current_user.print_my_courses()

    # instructor functions

    elif current_user.accountType == "Instructor" and command == "assign":  # instructor only courses
        # assign self to teach course
        print("Enter the CRN of the course you will be teaching")
        CRN = input(">")
        current_user.assign_course_instructor(CRN)

    elif current_user.accountType == "Instructor" and command == "remove":
        # remove self from teaching course
        print("Enter CRN of the course you are no longer teaching")
        CRN = input(">")
        current_user.remove_course_instructor(CRN)

    elif current_user.accountType == "Instructor" and command == "roaster":
        current_user.print_course_roaster()


    # admin functions

    elif current_user.accountType == "Admin" and command == "create_user":
        # create new user
        print("What type of user are you creating?")
        print("1 - Student")
        print("2 - Instructor")
        print("3 - Admin")
        type = input(">")

        print("Enter First Name")
        firstName = input(">")
        print("Enter Last Name:")
        lastName = input(">")
        if type == "1":  # student account
            print("Enter Major (or NULL):")
            major = input(">")
            if major == "NULL" or major == "":
                major = None
            print("Enter Grad Year (or NULL):")
            gradYear = input(">")
            if gradYear == "NULL" or major == "" or not isinstance(gradYear, int):
                gradYear = None

            current_user.create_new_user(firstName, lastName, "Student", major=major, gradYear=gradYear)

        elif type == "2":  # instructor account
            print("Enter dept (or NULL):")
            dept = input(">")
            if dept == "NULL" or dept == "":
                dept = None
            print("Enter hire year (or NULL):")
            hireYear = input(">")
            if hireYear == "Null" or hireYear == "" or not isinstance(hireYear, int):
                hireYear = None

            current_user.create_new_user(firstName, lastName, "Instructor", dept=dept, hireYear=hireYear)

        elif type == "3":  # admin account
            print("Enter office (or NULL):")
            office = input(">")
            if office == "Null" or office == "":
                office = None

            current_user.create_new_user(firstName, lastName, "Admin", office=office)

    elif current_user.accountType == "Admin" and command == "delete_user":
        # delete a user from the database

        # most of this function should really be converted to an Admin method delete_user()

        print("Enter ID of account to be deleted")
        current_user.delete_user(input(">"))


    else:
        print("Not a valid command - read carefully this time")

    # end of the gigantic if...elif... statement

    return menu(current_user)


def main(commit=False):  # main defaults to not committing the changes. run main(true) to commit
    print("Welcome to the School Database System")
    print("=====================================")
    print("Enter 1 to login to your account")
    print("Enter 2 to access system as a guest")
    print("Enter 3 to exit")
    selection = input(">")

    if selection == "1":
        current_user = login_menu()
        if current_user is None:
            print("\n\n")
            return main(commit)
        else:
            print("Login Successful - User type: " + current_user.accountType)
            print("Welcome, " + current_user.firstName)

    elif selection == "2":
        current_user = Guest()
    elif selection == "3":
        print("Exiting...")
        return
    else:
        print("Not a valid command")
        return main(commit)

    menu(current_user)
    if commit:
        db.commit()
        db.close()


if __name__ == '__main__':
    main()
