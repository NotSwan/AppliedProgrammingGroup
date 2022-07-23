import user_classes


def login():
    username = input("Enter username:")
    if (db.execute("SELECT ID FROM Logins WHERE username = '" + username + "'")).fetchone() is None:
        print("User does not exist")
        return None

    password = str((db.execute("SELECT password FROM Logins WHERE username = '" + username + "'")).fetchone()[0])
    print(password)

    while password == "None":
        print("New user detected")
        new_pass1 = input("Set password:")
        new_pass2 = input("Confirm password:")
        if new_pass1 == new_pass2:
            password = new_pass1
            db.execute("UPDATE Logins SET password = '" + password + "' WHERE username ='" + username + "'")
            print("Password set successfully")
            return login()
        else:
            print("Passwords must match")

    attempts = 0
    while attempts < 5:
        entered_pass = input("Enter password:")
        attempts = attempts + 1
        if entered_pass == password:
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
                print("hello")
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


current_user = login()
if current_user is not None:
    current_user.print_user_info()
