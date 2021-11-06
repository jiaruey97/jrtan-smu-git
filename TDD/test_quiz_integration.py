import unittest
import flask_testing
import json
from app import app, db, Quiz, Course, Instructor, Class, User_Database

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


class TestCreateQuiz(TestApp):
    def test_create_quiz(self):

        date_object = datetime.datetime.now()
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(c1)
        db.session.add(i1)
        db.session.add(u1)
        db.session.add(cl1)

        db.session.commit()

        request_body = {
            "Course_ID": c1.Course_ID,
            "Instructor_ID": i1.Instructor_ID,
            "Section": 12,
            "Question_Object": "Chickeasd",
            "Class_ID": cl1.Class_ID,
            "Timing": "1.5hr"
        }

        response = self.client.post("/create_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "Course_ID": 1,
                "Instructor_ID": 1,
                "Section": 12,
                "Question_Object": "Chickeasd",
                "Class_ID": 1,
                "Quiz_ID": 1,
                "Timing": "1.5hr"}
        })

    def test_create_quiz_invalid_Instructor(self):
        date_object = datetime.datetime.now()
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(c1)
        db.session.add(cl1)
        db.session.commit()

        request_body = {
            "Course_ID": c1.Course_ID,
            "Instructor_ID": 2,
            "Section": 12,
            "Question_Object": "Chickeasd",
            "Class_ID": cl1.Class_ID,
            "Timing": "1.5hr"
        }

        response = self.client.post("/create_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "Instructor not valid."
        })

    def test_create_quiz_invalid_Course(self):

        date_object = datetime.datetime.now()

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(i1)
        db.session.add(cl1)
        db.session.add(u1)
        db.session.commit()

        request_body = {
            "Course_ID": 1,
            "Instructor_ID": i1.Instructor_ID,
            "Section": 12,
            "Question_Object": "Chickeasd",
            "Class_ID": cl1.Class_ID,
            "Timing": "1.5hr"
        }

        response = self.client.post("/create_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "Course not valid."
        })

    def test_create_quiz_invalid_Class(self):

        date_object = datetime.datetime.now()

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(i1)
        db.session.add(c1)
        db.session.add(u1)
        db.session.commit()

        request_body = {
            "Course_ID": c1.Course_ID,
            "Instructor_ID": i1.Instructor_ID,
            "Section": 12,
            "Question_Object": "Chickeasd",
            "Class_ID": 2,
            "Timing": "1.5hr"
        }

        response = self.client.post("/create_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "Class not valid."
        })


class TestQuizRetrieveByID(TestApp):
    def test_retrieve_quiz_id(self):
        date_object = datetime.datetime.now()
        q1 = Quiz(Course_ID=1, Instructor_ID=1,
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Timing="23")
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(q1)
        db.session.add(u1)
        db.session.add(c1)
        db.session.add(i1)
        db.session.add(cl1)
        db.session.commit()

        id = i1.Instructor_ID

        response = self.client.get("/spm/quiz_retrieve/{0}".format(id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Course_ID": 1,
                "Instructor_ID": 1,
                "Section": 1,
                "Question_Object": "Chickensds",
                "Class_ID": 1,
                "Quiz_ID": 1,
                "Timing": "23"
            }
        })

    def test_retrieve_quiz_id_nothing(self):
        id = 1
        response = self.client.get("/spm/quiz_retrieve/{0}".format(id))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "message": "Quiz Not Found not found."
        })


class TestQuizRetrieve(TestApp):
    def test_retrieve_all_quiz(self):
        date_object = datetime.datetime.now()
        q1 = Quiz(Course_ID=1, Instructor_ID=1,
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Timing="23")
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(q1)
        db.session.add(u1)
        db.session.add(c1)
        db.session.add(i1)
        db.session.add(cl1)
        db.session.commit()
        response = self.client.get("spm/quiz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "quiz": [{
                    "Course_ID": 1,
                    "Instructor_ID": 1,
                    "Section": 1,
                    "Question_Object": "Chickensds",
                    "Class_ID": 1,
                    "Quiz_ID": 1,
                    "Timing": "23"
                }]
            }
        })

    def test_retrieve_all_quiz_nothing(self):
        response = self.client.get("spm/quiz")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no quiz."
        })


class TestQuizRetrieveByInstructor(TestApp):
    def test_retrieve_quiz_instructor(self):
        date_object = datetime.datetime.now()
        q1 = Quiz(Course_ID=1, Instructor_ID=1,
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Timing="23")
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(q1)
        db.session.add(u1)
        db.session.add(c1)
        db.session.add(i1)
        db.session.add(cl1)
        db.session.commit()

        id = 1
        response = self.client.get("/spm/quiz/{0}".format(id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "quiz": [{
                    "Course_ID": 1,
                    "Instructor_ID": 1,
                    "Section": 1,
                    "Question_Object": "Chickensds",
                    "Class_ID": 1,
                    "Quiz_ID": 1,
                    "Timing": "23"
                }]
            }
        })

    def test_retrieve_quiz_instructor_nothing(self):
        id = 1
        response = self.client.get("/spm/quiz/{0}".format(id))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "message": "Quiz Not Found not found."
        })


class TestQuizDelete(TestApp):
    def test_retrieve_quiz_instructor(self):
        date_object = datetime.datetime.now()
        q1 = Quiz(Course_ID=1, Instructor_ID=1,
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Timing="23")
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(q1)
        db.session.add(u1)
        db.session.add(c1)
        db.session.add(i1)
        db.session.add(cl1)
        db.session.commit()

        id = q1.Quiz_ID
        response = self.client.post("/quiz/delete/{0}".format(id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "message": "Delete Successful"
        })

    def test_retrieve_quiz_delete_fail(self):
        id = 10
        response = self.client.post("/quiz/delete/{0}".format(id))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "message": "Oops somethign went wrong"
        })


class TestQuizUpdate(TestApp):
    def test_quiz_update(self):
        date_object = datetime.datetime.now()
        q1 = Quiz(Course_ID=1, Instructor_ID=1,
                Section=1, Question_Object='Chickensds', Class_ID=1,
                Timing="23")
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        cl1 = Class(Class_ID=1, Class_Name='Ducky',
                    Class_Details='UKM123', Size=5, Current_Size=2,
                    Course_ID=1, Instructor_ID=1,
                    Start_Time=date_object, End_Time=date_object, Sections=4, Students="Hello")

        db.session.add(q1)
        db.session.add(u1)
        db.session.add(c1)
        db.session.add(i1)
        db.session.add(cl1)
        db.session.commit()

        id = q1.Quiz_ID

        request_body = {
            "Question_Object": "Ducky",
        }

        response = self.client.post("/quiz/{0}/update".format(id),
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "message": "Update Successful"
        })

    def test_quiz_update_fail(self):
        id = 10

        request_body = {
            "Question_Object": "Ducky",
        }
        response = self.client.post("/quiz/{0}/update".format(id),
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "No Such Quiz Exist!"
        })


if __name__ == '__main__':
    unittest.main()
