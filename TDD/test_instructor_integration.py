import unittest
import flask_testing
import json
from app import app, db, Instructor, User_Database

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


class TestInstructorRetrieve(TestApp):
    def test_retrieve_instructor(self):
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        i1 = Instructor(Instructor_ID=1, Actual_Name='Ducky',
                    Username='UKM123')

        db.session.add(u1)
        db.session.add(i1)
        db.session.commit()

        response = self.client.get("/spm/instructor")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "instructor": [{"Instructor_ID": 1,
                "Actual_Name": "Ducky",
                "Username": "UKM123"}]
            }
        })


class TestInstructorCreate(TestApp):
    def test_create_instructor(self):
        u1 = User_Database(Username="UKM123", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(u1)
        db.session.commit()

        request_body = {
            "Instructor_ID": 1,
            "Actual_Name": "Ducky",
            "Username": "UKM123"
        }

        response = self.client.post("/create_instructor",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "Instructor_ID": 1,
                "Actual_Name": "Ducky",
                "Username": "UKM123"
            }
        })

    def test_create_instructor_no_user(self):

        request_body = {
            "Instructor_ID": 1,
            "Actual_Name": "Ducky",
            "Username": "UKM123"
        }

        response = self.client.post("/create_instructor",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "code": 500,
            "message": "User not valid."
        })


if __name__ == '__main__':
    unittest.main()
