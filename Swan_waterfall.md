# Waterfall process method

## Table of Contents
- [Waterfall process method](#waterfall-process-method)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Design](#design)
    - [Design restraints](#design-restraints)
  - [Implement](#implement)
  - [Integration and test](#integration-and-test)
  - [Operation and maitenance](#operation-and-maitenance)
___
## Requirements
To fulfill the contract we must meet this strict metrics
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
  + Thoroughly test to ensure stability
___
## Design

### Design restraints
+ A base class of user containing ID and name
  + Must also contain set functions for all values alongside a print function
+ Inhereting from user and with class specific attributes and get/set functions accordingly
  + Student will have functions for printing the schedule, add/drop courses, and course search
  + Instructor will have functions for printing their schedule, print their class list, and course search
  + Admin will have functions that add courses, remove courses, add/remove users, add/remove student from a course, and to search and print rosters and courses.

The database that stores these users will be able to store: 
`100 Students, 10 Instructors, and 1 Admin users`

*The structure of the data stored and structure of the database and how they are interacted with would be fleshed out here*
___
## Implement
Aquisition of hardware, development of data types and the user interface, and the creation of the database would occur here
___
## Integration and test
Test data would be populated such that functionality can be tested and thoroughly vetted to ensure customer satisfaction
___

## Operation and maitenance
Once deployed the customer is given the finished product to rollout for use and if issues are discovered if communicated back to us will be reproduced and fixed to be deployed to the user.