import sqlite3 as sql

db = sql.connect("data2.db")


class User:
    def __init__(self, firstName, lastName, ID):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName
        self.ID = ID
        self.username = (lastName + firstName[0]).lower()
        self.email = self.username + "@wit.edu"

    def print_user_info(self):
        print("Name: " + self.fullName)
        print("ID: " + self.ID)
        print("Email: " + self.email)


class Instructor(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.dept = None
        self.hireYear = None

    def set_dept(self, dept):
        self.dept = dept

    def set_hireYear(self, hireYear):
        self.hireYear = hireYear

    def print_course_roaster(self):
        sql = str("SELECT * FROM Courses WHERE instructor ='" + self.lastName + "'")
        print(sql)
        for row in db.execute(sql).fetchall():
            print(row)


class Student(User):
    def __init__(self, firstName, lastName, id, gradYear=None, major=None):
        User.__init__(self, firstName, lastName, id)
        self.gradYear = gradYear
        self.major = major

    def set_gradYear(self, gradYear):
        self.gradYear = gradYear

    def set_major(self, major):
        self.major = major


class Admin(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.office = None

    def set_office(self, office):
        self.office = office

    def update_field(self, table, pri_key, field, new_value):
        if table == 'Courses':
            pri_key_field = 'CRN'
        else:
            pri_key_field = 'ID'

        sql = "UPDATE " + table + " SET " + field + " = '" + new_value + "' WHERE " + pri_key_field + " = " + pri_key
        print(sql)
        db.execute(sql)

    def create_new_user(self, firstName, lastName, accountType,
                        office=None, dept=None, hireYear=None, major=None, gradYear=None):
        username = (str(lastName + firstName[0])).lower()
        ID = str((db.execute("SELECT ID FROM Logins ORDER BY ID DESC")).fetchone()[0] + 1)
        sql = str("INSERT INTO Logins (ID, accountType, username) VALUES ("
                  + ID + ", '" + accountType + "', '" + username + "')")
        print(sql)
        db.execute(sql)

        # new users do not get assigned a password
        # password assignment is resolved on first login attempt

        if accountType == "Admin":
            sql = str("INSERT INTO Admin (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        if accountType == "Instructor":
            sql = str("INSERT INTO Instructors (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        if accountType == "Student":
            sql = str("INSERT INTO Students (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        print(sql)
        db.execute(sql)

    def create_new_course(self, title, time, days, year, credits, dept):
        CRN = str((db.execute("SELECT CRN FROM Courses ORDER BY CRN DESC")).fetchone()[0] + 1)

        sql = str("INSERT INTO Courses (CRN, title, time, days, year, credits, dept) VALUES (" +
                  str(CRN) + ", '" + title + "', " + str(time) + ", '" + days + "', " + str(year)
                  + ", " + str(credits) + ", '" + dept + "')")
        print(sql)
        db.execute(sql)


i = Instructor("George", "Gomez", 6)
i.print_course_roaster()
