import sqlite3 as sql

try:
    # works for Erik's IDE
    db = sql.connect("data2.db")
except:
    try:
        # works for Tyler's IDE
        db = sql.connect("School Database System/data2.db")
    except:
        print("database could not be located - check local directory")


def run_sql(sql, suppress=False):
    # in addition to running the sql and printing to the standard output
    # also outputs a list containing each line in the sqlite output
    # and every method that calls run_sql returns that same output
    # will be much more practical for testing


    try:
        result = db.execute(sql).fetchall()
        total = ""
        if result and not suppress:  # if list is not empty
            for row in result:
                data = str(row)
                data = data.replace("(", "")
                data = data.replace(")", "")
                data = data.replace("'", "")
                total += (data + "\n")

        return total

    except Exception as e:
        print("SQLite error:")
        print(e)
        return e


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
        return run_sql("SELECT * FROM Courses ORDER BY CRN ASC")

    def search_courses(self, field, search_value):
        sql = str("SELECT * FROM Courses WHERE " + field + " = '" + search_value + "' ORDER BY CRN ASC")
        return run_sql(sql)


class Guest(User):
    def __init__(self):
        User.__init__(self, "Guest", "User", 0)
        self.email = "N/A"


class Instructor(User):
    def __init__(self, firstName, lastName, id):
        User.__init__(self, firstName, lastName, id)
        self.dept = None
        self.hireYear = None

    def set_dept(self, dept):
        self.dept = dept

    def set_hireYear(self, hireYear):
        self.hireYear = hireYear

    def assign_course_instructor(self, CRN):
        sql = str("UPDATE Courses SET instructor = '" + self.lastName + "' WHERE CRN = " + str(CRN))
        run_sql(sql)

    def remove_course_instructor(self, CRN):
        sql = str("SELECT * FROM Courses WHERE instructor = '" + self.lastName +
                  "' AND CRN = " + str(CRN))

        if not run_sql(sql): # if no results
            print("You are not currently teaching that course")
        else:
            sql = str("UPDATE Courses SET instructor = NULL WHERE CRN = " + str(CRN))
            run_sql(sql)

    def print_course_roaster(self):
        sql = str("SELECT * FROM Courses WHERE instructor = '" + self.lastName + "'")
        return run_sql(sql)


class Student(User):
    def __init__(self, firstName, lastName, id, gradYear=None, major=None):
        User.__init__(self, firstName, lastName, id)
        self.gradYear = gradYear
        self.major = major

    def set_gradYear(self, gradYear):
        self.gradYear = gradYear

    def set_major(self, major):
        self.major = major

    def enroll(self, CRN):
        check_next_id = run_sql("SELECT enrollment_ID FROM Enrollment ORDER BY enrollment_ID DESC", suppress=True)

        if not check_next_id:
            enrollment_id = 1
        else:
            enrollment_id = str((check_next_id[0][0] + 1))

        sql = str("INSERT INTO Enrollment (enrollment_ID, CRN, student_ID, student_name) VALUES ("
                  + str(enrollment_id) + ", " + str(CRN) + ", " + str(self.ID) + ", '" + self.fullName + "')")
        run_sql(sql)

    def drop(self, CRN):
        sql = str("DELETE FROM Enrollment WHERE CRN = " + str(CRN) + " AND student_id = " + str(self.ID))
        run_sql(sql)

    def print_my_courses(self):
        sql = str("SELECT Enrollment.CRN, Courses.title, Courses.time, Courses.days, Courses.instructor "
                  + "from Enrollment INNER JOIN Courses ON Enrollment.CRN = Courses.CRN "
                  + "WHERE Enrollment.Student_ID = " + self.ID)
        return run_sql(sql)


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
        run_sql(sql)

    def create_new_user(self, firstName, lastName, new_accountType,
                        office=None, dept=None, hireYear=None, major=None, gradYear=None):
        username = (str(lastName + firstName))

        ID = str(run_sql("SELECT ID FROM Logins ORDER BY ID DESC", suppress=True))
        sql = str("INSERT INTO Logins (ID, accountType, username) VALUES ("
                  + ID + ", '" + new_accountType + "', '" + username.lower() + "')")
        run_sql(sql)

        # new users do not get assigned a password
        # password assignment is resolved on first login attempt

        if new_accountType == "Admin":
            sql = str("INSERT INTO Admin (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            run_sql(sql)
            if office is not None:
                self.update_field("Admin", ID, "office", office)

        if new_accountType == "Instructor":
            sql = str("INSERT INTO Instructors (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            run_sql(sql)
            if dept is not None:
                self.update_field("Instructors", ID, "dept", dept)
            if hireYear is not None:
                self.update_field("Instructors", ID, "hireYear", hireYear)

        if new_accountType == "Student":
            sql = str("INSERT INTO Students (ID, firstName, lastName, email) VALUES ("
                      + ID + ", '" + firstName + "', '" + lastName + "', '" + username + "@wit.edu')")
            run_sql(sql)
            if major is not None:
                self.update_field("Students", ID, "major", major)
            if gradYear is not None:
                self.update_field("Students", ID, "gradYear", gradYear)


    def create_new_course(self, title, time, days, year, credits, dept):
        CRN = str(run_sql("SELECT CRN FROM Courses ORDER BY CRN DESC", suppress=True)[0][0] + 1)

        sql = str("INSERT INTO Courses (CRN, title, time, days, year, credits, dept) VALUES (" +
                  str(CRN) + ", '" + title + "', " + str(time) + ", '" + days + "', " + str(year)
                  + ", " + str(credits) + ", '" + dept + "')")
        return run_sql(sql)

    def remove_entry(self, table, pri_key):
        if table == 'Courses':
            pri_key_field = 'CRN'
        else:
            pri_key_field = 'ID'

        sql = str("DELETE FROM " + table + " WHERE " + pri_key_field + " = " + str(pri_key))
        return run_sql(sql)

    def delete_user(self, ID):
        sql = str("SELECT accountType FROM Logins WHERE ID = " + str(ID))
        accountType = str(run_sql(sql)[0])
        self.remove_entry("Logins", ID)
        if accountType == "Student":
            table = "Students"
            sql = str("DELETE FROM Enrollment WHERE student_ID = " + str(ID))
            sql_output = run_sql(sql)
        elif accountType == "Instructor":
            table = "Instructors"
            lastName = run_sql(str("SELECT lastName from Instructors WHERE ID = " + str(ID)))[0]
            sql = str("UPDATE Courses SET instructor = NULL WHERE instructor = '" + lastName + "'")
            sql_output = run_sql(sql)
        elif accountType == "Admin":
            table = "Admin"
            sql_output = []
        else:
            return
        return sql_output.extend(self.remove_entry(table, ID))


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
