create schema if not EXISTS SPM;

use spm;

/*Course is Final should not be touch*/

create table if not EXISTS Course (
  Course_ID int NOT NULL,
  Course_Name varchar(255)  NOT NULL,
  Course_Details varchar(255)  NOT NULL,
  Duration varchar(255)  NOT NULL, 
  Prerequestic varchar(255)  NOT NULL, 
  Start_Time DATETIME  NOT NULL, 
  End_Time DATETIME  NOT NULL, 
  Sections int NOT NULL, 
  PRIMARY KEY (Course_ID)
);

/*Course can have as many class as it needs*/

create table if not EXISTS Class (
  Class_ID int  NOT NULL,
  Class_Name varchar(255)  NOT NULL,
  Class_Details varchar(255)  NOT NULL,
  Size int  NOT NULL,
  Current_Size int, 
  Course_ID int  NOT NULL, 
  Instructor_ID int, 
  Start_Time DATETIME  NOT NULL, 
  End_Time DATETIME  NOT NULL, 
  PRIMARY KEY (Class_ID),
  FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);

/*Instructor ID is not a Foreign Key Deleting A Instructor 
should not delete the Class But we must remove the 
Instructor Manually*/

create table if not EXISTS Instructor(
  Instructor_ID int  NOT NULL,
  LastName varchar(255)  NOT NULL,
  FirstName varchar(255)  NOT NULL,
  PRIMARY KEY (Instructor_ID)
);

/*Instructor to be added from User_Database*/

create table if not EXISTS User_Database(
  Username varchar(50) NOT NULL,
  Actual_Name varchar(255)  NOT NULL,
  Designation varchar(255)  NOT NULL,
  Department varchar(255)  NOT NULL,
  Current_Role varchar(255)  NOT NULL,
  Course_Assigned varchar(255),
  Course_Completed varchar(255),
  PRIMARY KEY (Username)
);

/*Should Be Prepopulated Already
Role will decide Access Right */

create table if not EXISTS Quiz (
  Quiz_ID int NOT NULL,
  Course_ID int  NOT NULL,
  Instructor_ID int NOT NULL,
  Section int NOT NULL,
  Question_Object varchar(255),
  PRIMARY KEY (Quiz_ID),
  FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
  FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
);

/*Section will not be tag as Foreign Key*/

create table if not EXISTS Quiz_Results(

  Quiz_Results_ID int NOT NULL,
  Username varchar(50) NOT NULL,
  Quiz_ID int NOT NULL,
  Course_ID int  NOT NULL,
  Section int NOT NULL,
  Marks int NOT NULL,
  Pass BOOLEAN NOT NULL,
  PRIMARY KEY (Quiz_Results_ID),
  FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
  FOREIGN KEY (Quiz_ID) REFERENCES Quiz(Instructor_ID),
  FOREIGN KEY (Username) REFERENCES User_Database(Username)
);

/*Pass can be used in web page generation
Quiz_Results_ID needed for Flask
*/

create table if not EXISTS Tracker(
  
  Tracker_ID int NOT NULL,
  Username varchar(50) NOT NULL,
  Course_ID int  NOT NULL,
  Class_ID int NOT NULL,
  Section_Object varchar(255) NOT NULL,
  PRIMARY KEY (Tracker_ID),
  FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
  FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID),
  FOREIGN KEY (Username) REFERENCES User_Database(Username)
);

/*Track Lesson Progress
Tracker_ID needed for Flask
*/

create table if not EXISTS Lesson_Materials(
  Lesson_Materials_ID int NOT NULL,
  Class_ID int NOT NULL,
  Section int NOT NULL,
  Lesson_Materials varchar(255) NOT NULL,
  PRIMARY KEY (Lesson_Materials_ID),
  FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID)
);

/*Material Generated will be based on Current Sections*/
