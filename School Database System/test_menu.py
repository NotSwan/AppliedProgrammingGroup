import builtins
import unittest
import user_classes
import io
import sys
import menu
from unittest.mock import patch

#  For each of the following functions:
#  Add/remove course from semester schedule (based on course ID number)
#  Assemble and print course roster (instructor)
#  Add/remove courses from the system (admin)
#  Log-in, log-out (all users)
#  Search all courses (all users) 
#  Search courses based on parameters (all users)

class Tester(unittest.TestCase):

    def setUp(self):
        self.user = user_classes.User('test','name',123)
        self.admin = user_classes.Admin('Erik','Haynes',1)
        self.instructor = user_classes.Instructor("Pat", "Lawlor", 2)
        self.maxDiff = None

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_print_user_info(self, expected_output, mock_stdout):
        self.user.print_user_info()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_user_info(self):
        self.assert_stdout_print_user_info('Name: test name\nID: 123\nEmail: namet@wit.edu\nAccount: Base User\n')

    def test_login_admin(self):
        self.assertIsInstance(menu.login("haynese","password","password"), user_classes.Admin)
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_print_roster(self, expected_output ,mock_stdout):
        self.instructor.print_course_roaster()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_roster(self):
        self.assert_stdout_print_roster("SQLite << SELECT * FROM Courses WHERE instructor = 'Lawlor'\n9, Mechanics 1, 900, MWF, 2022, 4, MECH, Lawlor\n10, Mechanics 2, 1030, MWF, 2022, 4, MECH, Lawlor\n11, Material Science, 1300, MWF, 2022, 4, MECH, Lawlor\n")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_search_all(self,expected_output ,mock_stdout):
        self.user.print_all_courses()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_search_all(self):
        self.assert_stdout_search_all("SQLite << SELECT * FROM Courses ORDER BY CRN ASC\n1, Intro to Engineering, 900, MWF, 2022, 4, ENGR, Anghelo\n\
2, Computer Science 1, 900, MWF, 2022, 4, COMP, Sheats\n\
3, Computer Science 2, 1030, MWF, 2022, 4, COMP, Sheats\n\
4, Calculus 1, 1030, MWF, 2022, 4, MATH, Ritchie\n\
5, Calculus 2, 1100, MWF, 2022, 4, MATH, Ritchie\n\
6, Physics 1, 1100, MWF, 2022, 4, PHYS, Elwin\n\
7, Physics 2, 1300, MWF, 2022, 4, PHYS, Elwin\n\
8, Thermodynamics, 1030, MWF, 2022, 4, PHYS, Elwin\n\
9, Mechanics 1, 900, MWF, 2022, 4, MECH, Lawlor\n\
10, Mechanics 2, 1030, MWF, 2022, 4, MECH, Lawlor\n\
11, Material Science, 1300, MWF, 2022, 4, MECH, Lawlor\n\
12, Network Theory 1, 900, MWF, 2022, 4, ELEC, Eddy\n\
13, Network Theory 2, 1030, MWF, 2022, 4, ELEC, Eddy\n\
14, Analog Circuit Design, 1300, MWF, 2022, 4, ELEC, Eddy\n\
15, Digital Circuit Design, 1500, MWF, 2022, 4, ELEC, Eddy\n\
16, English 1, 1000, TR, 2022, 4, HUMN, Popadiuk\n\
17, English 2, 1300, TR, 2022, 4, HUMN, Popadiuk\n\
18, Buisness Managment, 900, TR, 2022, 4, MGMT, Gomez\n\
19, Entrepreneurship, 1130, TR, 2022, 4, MGMT, Gomez\n")





if __name__ == '__main__':
    unittest.main()