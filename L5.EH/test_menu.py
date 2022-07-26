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

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_print_user_info(self, expected_output, mock_stdout):
        self.user.print_user_info()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_user_info(self):
        self.assert_stdout_print_user_info('Name: test name\nID: 123\nEmail: namet@wit.edu\nAccount: Base User\n')

    def test_login(self):
        self.assertIsInstance(menu.login("haynese","password"), user_classes.Admin)


if __name__ == '__main__':
    unittest.main()