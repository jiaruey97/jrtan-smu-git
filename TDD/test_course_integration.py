import unittest
import flask_testing
import json
from app import app, db, Course

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


class TestRetrieveCourse(TestApp):
    def test_retrieve_course(self):     
        date_object = datetime.datetime.now()
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/spm/course")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_course_by_ID(self):     
        date_object = datetime.datetime.now()
        c1 = Course(Course_ID=1, Course_Name='Ducky',
                    Course_Details='UKM123', Duration='3hr', Prerequestic='123',
                    Start_Time=date_object, End_Time=date_object, Sections=4)

        db.session.add(c1)
        db.session.commit()
        response = self.client.get("spm/course_retrieve/{0}".format(c1.Course_ID))
        self.assertEqual(response.status_code, 200)
 


if __name__ == '__main__':
    unittest.main()
