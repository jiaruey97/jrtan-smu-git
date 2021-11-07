import unittest
import flask_testing
import json
from app import app, db, Instructor, User_Database, Quiz, Quiz_Results, Class, Course

import datetime

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestResultRetrieve(TestApp):
    def test_retrieve_result(self):   
        date_object = datetime.datetime.now()
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        q1 = Quiz(Course_ID=1, Instructor_ID = 1, 
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Time="23")

        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequisite='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                     Username='UKM123')

        cl1 = Class(Class_ID = 1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID = 1, Instructor_ID = 1,
                    Start_Time=date_object, End_Time=date_object, Sections= 4, Students = "Hello")
        
        r1 = Quiz_Results(Username="UKM123",Quiz_ID = 1, Course_ID = 1, Section = "1", Marks = 12, Pass = False )


        db.session.add(u1)
        db.session.add(c1)
        db.session.add(q1)
        db.session.add(cl1)
        db.session.add(i1)
        db.session.add(r1)
        db.session.commit()

        response = self.client.get("/spm/results")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                        "quiz_results": [{
                                    "Quiz_Results_ID": 1,
                                    "Username":"UKM123",
                                    "Quiz_ID": 1, 
                                    "Course_ID" : 1, 
                                    "Section" : "1", 
                                    "Marks" : 12, 
                                    "Pass" : False}]
            }
                    })

class TestResultsCreate(TestApp):
    def test_create_result(self):   
        date_object = datetime.datetime.now()
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        q1 = Quiz(Course_ID=1, Instructor_ID = 1, 
                Section="1", Question_Object='Chickensds', Class_ID=1,
                Time="23")

        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequisite='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                     Username='UKM123')

        cl1 = Class(Class_ID = 1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID = 1, Instructor_ID = 1,
                    Start_Time=date_object, End_Time=date_object, Sections= 4, Students = "Hello")
        

        db.session.add(u1)
        db.session.add(c1)
        db.session.add(q1)
        db.session.add(cl1)
        db.session.add(i1)

        db.session.commit()

        request_body = {
                    
                    "Username":u1.Username,
                    "Quiz_ID": 1, 
                    "Course_ID" : c1.Course_ID, 
                    "Section" : "1", 
                    "Marks" : 12, 
                    "Pass" : False
        }
        

        response = self.client.post("/create_results",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                    "Quiz_Results_ID": 1,
                    "Username":"UKM123",
                    "Quiz_ID": 1, 
                    "Course_ID" : 1, 
                    "Section" : "1", 
                    "Marks" : 12, 
                    "Pass" : False}
                    })

    def test_create_result_invalid_Course(self):   
        date_object = datetime.datetime.now()
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        q1 = Quiz(Course_ID=1, Instructor_ID = 1, 
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Time="23")

        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequisite='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                     Username='UKM123')

        cl1 = Class(Class_ID = 1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID = 1, Instructor_ID = 1,
                    Start_Time=date_object, End_Time=date_object, Sections= 4, Students = "Hello")
        

        db.session.add(u1)
        db.session.add(c1)
        db.session.add(q1)
        db.session.add(cl1)
        db.session.add(i1)

        db.session.commit()

        request_body = {
                    
                    "Username":u1.Username,
                    "Quiz_ID": 1, 
                    "Course_ID" : 20, 
                    "Section" : 1, 
                    "Marks" : 12, 
                    "Pass" : False
        }
        response = self.client.post("/create_results",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "Course not valid."
                    })
 
    def test_create_result_invalid_Quiz(self):   
        date_object = datetime.datetime.now()
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")


        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequisite='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)


        db.session.add(u1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
                    
                    "Username":u1.Username,
                    "Quiz_ID": 1, 
                    "Course_ID" : c1.Course_ID, 
                    "Section" : 1, 
                    "Marks" : 12, 
                    "Pass" : False
        }

        response = self.client.post("/create_results",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "Quiz not valid."
                    })


    def test_create_result_invalid_User(self):   
        date_object = datetime.datetime.now()
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        q1 = Quiz(Course_ID=1, Instructor_ID = 1, 
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Time="23")

        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequisite='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                     Username='UKM123')

        cl1 = Class(Class_ID = 1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID = 1, Instructor_ID = 1,
                    Start_Time=date_object, End_Time=date_object, Sections= 4, Students = "Hello")
        

        db.session.add(u1)
        db.session.add(c1)
        db.session.add(q1)
        db.session.add(cl1)
        db.session.add(i1)


        db.session.commit()

        request_body = {
                    
                    "Username":"asadsadsa",
                    "Quiz_ID": 1, 
                    "Course_ID" : c1.Course_ID, 
                    "Section" : 1, 
                    "Marks" : 12, 
                    "Pass" : False
        }

        response = self.client.post("/create_results",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "User not valid."
                    })


if __name__ == '__main__':
    unittest.main()
