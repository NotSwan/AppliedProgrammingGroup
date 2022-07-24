from user_classes import *


def login():
    print("Enter username:")
    username = input(">")
    if username == "/x":
        return None

    if (db.execute("SELECT ID FROM Logins WHERE username = '" + username.lower() + "'")).fetchone() is None:
        print("User does not exist")
        print("Enter /x to return to exit")
        return login()

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
            return login()
        else:
            print("Passwords must match")

    attempts = 0
    while attempts < 5:
        print("Enter password:")
        entered_pass = input(">")
        attempts = attempts + 1
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
        else:
            print("Incorrect Password")
            print(str(5 - attempts) + " attempts remaining")

    print("Too many failed password attempts")
    print("Exiting...")
    return None


def logout():
    global current_user
    current_user = Guest()


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
        print("roster - view the classes you are currently enrolled in")

    if current_user.accountType == "Instructor":
        print("assign - assign self to course")
        print("remove - remove self from course")

    if current_user.accountType == "Admin":
        print("create_user - create a new user")
        print("delete_user - delete a user")
        print("create_course - create a new course")
        print("delete_course - delete a course")
        print("enroll_student - enroll a student in a course")
        print("drop_student - drop a course from a student's roaster")
        print("search_table - search any table")

    print("logout - exit the system")

    action = input(">")

    if action == "view":
        current_user.print_all_courses()
        menu_return(current_user)
    elif action == "search":
        print("What field do you want to search by? (CRN, title, days, year, credits, dept, instructor)")
        field = input(">")
        print("Enter search term")
        search = input(">")
        current_user.search_courses(field, search)
        menu_return(current_user)
    elif action == "logout":
        print("Logging out...")
        return main()


def main():
    print("Welcome to the School Database System")
    print("=====================================")
    print("Enter 1 to login to your account")
    print("Enter 2 to access system as a guest")
    print("Enter 3 to exit")
    selection = input(">")

    if selection == "1":
        current_user = login()
        if current_user is None:
            print("/n/n")
            return main()
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
        return main()

    menu(current_user)


main()
