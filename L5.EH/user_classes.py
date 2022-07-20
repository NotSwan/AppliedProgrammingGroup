import sqlite3 as sql

db = sql.connect("data2.db")


def fetchone_and_cleanup(result):
    print(result.fetchone()[0])


class User:
    def __init__(self, firstName, lastName, id):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName
        self.id = id
        self.email = lastName + firstName[0] + "@wit.edu"


class Student(User):
    def __init__(self, firstName, lastName, id, gradYear, major):
        User.__init__(self, firstName, lastName, id)
        self.gradYear = gradYear
        self.major = major


class Instructor(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.dept = None
        self.hireYear = None
        self.courseList = []  # later these lists should be in the database, not the object


class Admin(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.office = None

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
        username = str(lastName + firstName[0])
        ID = str((db.execute("SELECT ID FROM Logins ORDER BY ID DESC")).fetchone()[0] + 1)
        sql = str("INSERT INTO Logins (ID, accountType, username) VALUES ("
                  + ID + ", '" + accountType + "', '" + username + "')")
        print(sql)
        db.execute(sql)

        # new users do not get assigned a password
        # password assignment should be resolved on first login attempt

        if accountType == "Admin":
            sql = str("INSERT INTO Admin (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            print(sql)
            db.execute(sql)
            if office is not None:
                self.update_field("Admin", ID, "office", office)

        if accountType == "Instructor":
            sql = str("INSERT INTO Instructors (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            print(sql)
            db.execute(sql)
            if dept is not None:
                self.update_field("Instructors", ID, "dept", dept)

            if hireYear is not None:
                self.update_field("Instructors", ID, "hireYear", str(hireYear))

        if accountType == "Student":
            sql = str("INSERT INTO Students (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            print(sql)
            db.execute(sql)
            if major is not None:
                self.update_field("Students", ID, "major", major)

            if gradYear is not None:
                self.update_field("Students", ID, "gradYear", str(gradYear))

    def create_new_course(self, title, time, days, year, credits, dept):
        CRN = str((db.execute("SELECT CRN FROM Courses ORDER BY ID DESC")).fetchone()[0] + 1)

        sql = str("INSERT INTO Courses (CRN, title, time, days, year, credits, dept) VALUES (" +
                  str(CRN) + ", '" + title + "', " + str(time) + ", '" + days + "', " + str(year)
                  + ", " + str(credits) + ", '" + dept + "')")
        print(sql)
        db.execute(sql)


db.close()
