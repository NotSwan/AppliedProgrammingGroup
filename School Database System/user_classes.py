import sqlite3 as sql

db = sql.connect("data2.db")


def run_sql(sql):
    print("SQLite << " + sql)
    try:
        result = db.execute(sql).fetchall()
        if result[0] is not None:
            for row in result:
                data = str(row)
                data = data.replace("(", "")
                data = data.replace(")", "")
                data = data.replace("'", "")
                print(data)

    except:
        print("SQLite returned an error")


class User:
    def __init__(self, firstName, lastName, ID):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName
        self.ID = ID
        self.username = (lastName + firstName[0]).lower()
        self.email = self.username + "@wit.edu"
        self.accountType = "Base User"

    def print_user_info(self):
        print("Name: " + self.fullName)
        print("ID: " + str(self.ID))
        print("Email: " + self.email)
        print("Account: " + self.accountType)

    def print_all_courses(self):
        run_sql("SELECT * FROM Courses ORDER BY CRN ASC")

    def search_courses(self, field, search_value):
        sql = str ("SELECT * FROM Courses WHERE " + field + " = '" + search_value + "' ORDER BY CRN ASC")
        run_sql(sql)


class Guest(User):
    def __init__(self):
        User.__init__(self, "Guest", "User", 0)
        self.email = "N/A"
        self.accountType = "Guest"


class Instructor(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.dept = None
        self.hireYear = None
        self.accountType = "Instructor"

    def set_dept(self, dept):
        self.dept = dept

    def set_hireYear(self, hireYear):
        self.hireYear = hireYear

    def print_course_roaster(self):
        sql = str("SELECT * FROM Courses WHERE instructor = '" + self.lastName + "'")
        run_sql(sql)


class Student(User):
    def __init__(self, firstName, lastName, id, gradYear=None, major=None):
        User.__init__(self, firstName, lastName, id)
        self.gradYear = gradYear
        self.major = major
        self.accountType = "Student"

    def set_gradYear(self, gradYear):
        self.gradYear = gradYear

    def set_major(self, major):
        self.major = major


class Admin(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.office = None
        self.accountType = "Admin"

    def set_office(self, office):
        self.office = office

    def update_field(self, table, pri_key, field, new_value):
        if table == 'Courses':
            pri_key_field = 'CRN'
        else:
            pri_key_field = 'ID'

        sql = "UPDATE " + table + " SET " + field + " = '" + new_value + "' WHERE " + pri_key_field + " = " + pri_key
        run_sql(sql)

    def create_new_user(self, firstName, lastName, new_accountType,
                        office=None, dept=None, hireYear=None, major=None, gradYear=None):
        username = (str(lastName + firstName[0]))
        ID = str((db.execute("SELECT ID FROM Logins ORDER BY ID DESC")).fetchone()[0] + 1)
        sql = str("INSERT INTO Logins (ID, accountType, username) VALUES ("
                  + ID + ", '" + new_accountType + "', '" + username.lower() + "')")
        run_sql(sql)

        # new users do not get assigned a password
        # password assignment is resolved on first login attempt

        if new_accountType == "Admin":
            sql = str("INSERT INTO Admin (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        if new_accountType == "Instructor":
            sql = str("INSERT INTO Instructors (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        if new_accountType == "Student":
            sql = str("INSERT INTO Students (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")

        run_sql(sql)

    def create_new_course(self, title, time, days, year, credits, dept):
        CRN = str((db.execute("SELECT CRN FROM Courses ORDER BY CRN DESC")).fetchone()[0] + 1)

        sql = str("INSERT INTO Courses (CRN, title, time, days, year, credits, dept) VALUES (" +
                  str(CRN) + ", '" + title + "', " + str(time) + ", '" + days + "', " + str(year)
                  + ", " + str(credits) + ", '" + dept + "')")
        run_sql(sql)

    def remove_entry(self, table, pri_key):
        if table == 'Courses':
            pri_key_field = 'CRN'
        else:
            pri_key_field = 'ID'

        sql = str("DELETE FROM " + table + " WHERE " + pri_key_field + " = " + pri_key)
        run_sql(sql)


class Sysadmin(Admin, Instructor, Student):
    # useful class for quickly making an object to test your methods
    def __init__(self):
        User.__init__(self, "sysadmin", "", -1)
        self.dept = None
        self.hireYear = None
        self.gradYear = None
        self.major = None
        self.office = None
        self.accountType = "Sysadmin"