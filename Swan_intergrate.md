# Intergrate process method

## Table of Contents
  - [Requirements](#requirements)
  - [Component Analysis](#component-analysis)
  - [Requirments Modification](#requirement-modification)
  - [System Design](#system-design)
  - [Develop & Intergrate](#development--integration)
  - [Validation](#validation)
___
## Requirements
To fulfill the contract we must meet these metrics
+ A database capable of 100 students 10 instrutors and 1 admin
+ A database of courses containing:
  + CRNs
  + Course Name
  + Times
  + Instructor
+ 3 Types of users
  + Admin - can see and edit everything
  + Student - can register and see available classes and their own schedule
  + Instructor - can see available courses and their own course roster
  + Support multiple semesters and printing out of schedules and scheduling preferences
___
## Component Analysis
Decide the level of customizability the customer wants such as if they want to use a full solution (MySchool, Kiddom, PCR Educator Management System, etc.) or would like to have a custom colution where a database management system as well as custom interfacing UI would have to be created.

## Requirement Modification
+ A base class of user containing ID and name
  + Must also contain set functions for all values alongside a print function
+ Inhereting from user and with class specific attributes and get/set functions accordingly
  + Student will have functions for printing the schedule, add/drop courses, and course search
  + Instructor will have functions for printing their schedule, print their class list, and course search
  + Admin will have functions that add courses, remove courses, add/remove users, add/remove student from a course, and to search and print rosters and courses.

The database that stores these users will be able to store if that has changed: 
`100 Students, 10 Instructors, and 1 Admin users`

*The structure of the data stored and structure of the database and how they are interacted with would be fleshed out here*
___
## System Design
Aquisition of hardware or hosting, development of data types and the user interface, and the creation of the database would occur here, or the configuration of specific DBMS with support.
___
## Development & Integration
Compatibility layers between software or specific hooks into the full solution may be developed to further meet spec. Test data would be populated such that functionality can be tested and thoroughly vetted to ensure customer satisfaction
___

## Validation
Once deployed the customer is given the finished product to rollout for use and if issues are discovered if communicated back to us will be reproduced and support can be given or direccted to the componenets support