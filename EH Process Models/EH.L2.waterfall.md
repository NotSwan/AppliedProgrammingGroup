Erik Haynes
# Lab 2 - Waterfall Model

![Waterfall Model](https://i.imgur.com/N8I2IQa.png)
## Requirements Analysis and Definition

 - Database of users: the system must work for 100 students, 10 instructors, and 1 admin
 - Database of courses: this will contain information such as the CRN, course name, times, and instructor
- Three types of users:
	- Student -  can register, can see available courses and their own schedule
	- Instructor – can see available courses and their own course roster
	- admin – can see everything, can edit courses, users, and schedules
- The system should include multiple semesters, print-out of schedule, scheduling preferences

## System Software and Design
- Pick a programming language for the program to be written in
  - This decision will be influenced by the requirements such as speed and maintainability 
- Establish what database software will be used to store all the data
- Pick user interface - desktop, browser or mobile application
- Locate current repository of student, instructor, admin, and course information to be imported to the new system
- Begin implementing the functionality outlined above

## Implementation and Unit Testing
- Build and test individual units of the program
	- Database
		- Import the current course information to the database
	- Admin functionality 
		- create, edit and remove courses, students, and instructors
		- access and print out course, student, and instructor information
	- Instructor functionality
		- view the courses they teach
		- view their schedule
	- Student functionality
		- register and unregister for classes
		- view their schedule

## Integration and System Testing

 - Combine the units and test the system as a whole
	 -  Create a login system to establish and enforce what permissions each user has
	- Test that the functionality established in the unit test still works in the integrated system
	- Test that users are unable to preform the actions of a user type they are not
	- Test for extraneous inputs and such error handling

## Operation and Maintenance
 - Roll out the System and listen for user feedback
 - Patch any bugs that may arise
 - Look for ways that the interface can be streamlined based on how the real users end up interacting with the system.