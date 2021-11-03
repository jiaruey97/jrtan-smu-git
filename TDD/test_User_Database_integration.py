import unittest
import flask_testing
import json
from app import app, db, User_Database

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


class TestRetrieveUser(TestApp):
    def test_retrieve_user(self):     
        c1 = User_Database(Username="Timmy", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/spm/user_database")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                        "user": [{
                            "Username":"Timmy",
                            "Actual_Name":"Ducky",
                            "Department":'UKM123',
                            "Current_Position":"hello",
                            "Course_Assigned": '123',
                            "Course_Completed":"date_object",
                            "Course_Pending": "Course_Pending"
                        }]
                    }
        })

    def test_retrieve_user_by_ID(self):     
        c1 = User_Database(Username="Timmy", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/user_database/{0}".format(c1.Username))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                        "user": [{
                            "Username":"Timmy",
                            "Actual_Name":"Ducky",
                            "Department":'UKM123',
                            "Current_Position":"hello",
                            "Course_Assigned": '123',
                            "Course_Completed":"date_object",
                            "Course_Pending": "Course_Pending"
                        }]
                    }
        })
 

class TestUpdateUser(TestApp):
     def test_retrieve_user_by_ID(self):     
        c1 = User_Database(Username="Timmy", Actual_Name='Ducky',
                    Department='UKM123', Current_Position='hello', Course_Assigned='123',
                    Course_Completed="date_object", Course_Pending="Course_Pending")

        db.session.add(c1)
        db.session.commit()

        request_body = {
            "Course_Pending":"Ducky",
        }

        response = self.client.post("/user_database/{0}/update".format(c1.Username), 
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "message": "Update Successful"
                    })
                          


if __name__ == '__main__':
    unittest.main()
