###############
#Citations
#https://www.w3schools.com/python/python_inheritance.asp
#https://stackoverflow.com/questions/23326099/how-can-i-limit-the-user-input-to-only-integers-in-python
#
###############
class User:
    "User Class with crediential information variables and set functions for each."
    def __init__(self, firstName = "testFirst", lastName = "testLast", id = 1234):
        self.firstName = firstName
        self.lastName = lastName
        self.id = id

    def set_first(self, firstName):
        self.firstName = firstName
    
    def set_last(self, lastName):
        self.lastName = lastName
    
    def set_id(self, id):
        self.id = id
    
    def get_user(self):
        print (f"\n{self.lastName} , {self.firstName} \nWIT ID: W00{self.id}")

    def debug(self):
        self.get_user()

class Student(User):
    "Child of User class that contains student specific functions"
    def __init__(self, firstName = "studentFirst", lastName = "studentLast", id = 1235):
        User.__init__(self, firstName, lastName, id)

    def debug(self):
        self.get_user()
        self.search_classes()
        self.add_drop_class()
        self.print_schedule()

    def search_classes(self):
        print ("This will search classes")

    def add_drop_class(self):
        print ("This will add/drop specified class")

    def print_schedule(self):
        print ("This will print the schedule")

class Instructor(User):
    "Child of User class that contains functionality pertaining to an Instructor"
    def __init__(self, firstName = "instructorFirst", lastName = "instructorLast", id = 1236):
        User.__init__(self, firstName, lastName, id)

    def debug(self):
        self.get_user()
        self.print_course_list()
        self.print_schedule()
        self.search_classes()

    def print_schedule(self):
        print ("This will print the schedule")

    def print_course_list(self):
        print ("This will print the course list")

    def search_classes(self):
        print ("This will search classes") 

class Admin(User):
    "Administration class inhereiting from User with relevant functionality"
    def __init__(self, firstName = "adminFirst", lastName = "adminLast", id = 1237):
        User.__init__(self, firstName, lastName, id)

    def debug(self):
        self.get_user()
        self.add_course()
        self.remove_course()
        self.add_remove_student()
        self.search_classes()

    def add_course(self, course):
        print ("This will add specified class")

    def remove_course(self, course):
        print ("This will remove specified class")
    
    def add_remove_student(self, student):
        print ("This will add/remove students")

    def search_course(self):
        print ("This will search courses and print their roster")



def prompt_for_usertype():
    print("To begin what type of user would you like to create?")
    print("1. User")
    print("2. Student")
    print("3. Instructor")
    print("4. Admin")
    print("0. Exit")

    while True:
        try:
            userType = int(input("Input usertype: "))
            if(userType >= 0 and userType < 5):
                return userType
            else:
                raise Exception("IntegerOutOfRange")
        except:
            print("Invalid input!")

def create_user(userType, users):
    if(userType != 0):
        print(f"\nYou selected: {userTypeDict.get(userType)}")
        print("Enter Credentials seperated by commas(,) as first,last,id")
        
        while True:
            try:
                a,b,c = input("Input credentials:").split(",")
                int(c)
                break
            except:
                print("Invalid input")
        if(userType == 1):
            users.append(User(a,b,c))
        if(userType == 2):
            users.append(Student(a,b,c))
        if(userType == 3):
            users.append(Instructor(a,b,c))
        if(userType == 4):
            users.append(Admin(a,b,c))


# menu(User[] users)
# 
#       The function containing all logic for entering the needed commands
#       Now for testing the menu relies on the debug function that calls all others
#       but when greater functionality is added proper expansion of the commands will be done
#      
#       Primary function is handling and restricting of inputs both of commands and for 
#       additional requirments within called commands
#     
def menu():
    print("\n------Main Menu------")
    print("4. Change credentials")
    print("5. Debug(calls all other commands)")
    print("0. Exit")

    while True:
        try:
            userInput = int(input("Input command: "))
            if(userInput >= 0 and userInput < 6):
                break
            else:
                raise Exception("IntegerOutOfRange")
        except:
            print("Invalid input!")

    if(userInput == 4):
        while True:
            try:
                print("Syntax: first,last,id")
                first,last,id = input("Input new credentials: ").split(",")
                int(id)
                break
            except:
                print("Incorrect input")
        users[0].set_first(first)
        users[0].set_last(last)
        users[0].set_id(id)

    if(userInput == 5):
        users[0].debug()
    return userInput



# __main__
#      
#      main function that does simple movement between functions
#      aswell as storing values input and objects created within 
#      some of the functions, stores global dictionary
#     
if __name__ == '__main__':
    global userTypeDict 
    userTypeDict= {
        1: "User",
        2: "Student",
        3: "Instructor",
        4: "Admin"
    }

    print("\t---Welcome to the User Creation Tool---")
    userInput = prompt_for_usertype()
    users = list()
    create_user(userInput, users)
    
    while userInput != 0:
        userInput = menu()
        
    print("Exiting...")