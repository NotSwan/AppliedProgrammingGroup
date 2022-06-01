Erik Haynes
# Lab 2 - Integrate and Configure
![Integration](https://i.imgur.com/9nJnb6o.png)
## Requirements and Specifications
 - Database of users: the system must work for 100 students, 10 instructors, and 1 admin
 - Database of courses: this will contain information such as the CRN, course name, times, and instructor
 - Three types of users:
	- Student -  can register, can see available courses and their own schedule
	- Instructor – can see available courses and their own course roster
	- admin – can see everything, can edit courses, users, and schedules
 - The system should include multiple semesters, print-out of schedule, scheduling preferences
  []: # (Nice list of everything thats needed - NN)
## Component Analysis
- Review existing School Administration software (Gradelink, DreamClass, MySchool, etc.)
	- Creating new software may be unnecessary if existing software fulfills the above requirements 
- Review existing database tools (MySQL, MongoDB, Oracle RDBMS, etc.)
	- Building a database from scratch is unnecessary when many database tools already exist
	- Assess if the existing solutions allow for expansions of features through development of extensions to allow for a best of both worlds approach if there is no one  pre existing solution that hits all the check boxes
## Requirements Modification
-Revise original program specs based on the functionality and limitations of the available software solutions
[]: # (add some specific examples maybe of how this can be done - NN)
## System Design with Reuse
- Design a system that implements the best suited tools found in the component analysis step, filling in any gaps in their functionality with new code
## Development and Integration
- Build the program around the components selected, interfacing with those program's APIs
- Test the software to ensure it is working as intended 
[]: # (What tests can you expect to use -  NN)
## System Validation
- Launch the system and wait for feedback from users
- Fix any bugs discovered after launch
- Monitor the external software used in the program to ensure that updates do not stop the program from working
 
