import unittest
import flask_testing
import json
from app import app, db, Lesson_Materials

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


class TestLessonMaterials(TestApp):
    def test_upload_course(self):
        #lm1 = Lesson_Materials(Lesson_Materials_ID=6, Course_ID=1, Lesson_Materials="something")

        # db.session.add(lm1)
        # db.session.commit()

        request_body = {
            "Lesson_Materials_ID": 6,
            "Course_ID": 1,
            "Lesson_Materials": "something"
        }
        lesson_materials_id = 1
        response = self.client.post("/update_materials/{0}".format(lesson_materials_id),
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "message": "It's a success!",
            "data": {
                "Course_ID": 1,
                "Lesson_Materials": "something",
                "Lesson_Materials_ID": 6,
            }

        })

    def test_retrieve_course(self):
        lm1 = Lesson_Materials(Lesson_Materials_ID=6,
                               Course_ID=1, Lesson_Materials="something")
        db.session.add(lm1)
        db.session.commit()

        course_id = lm1.Course_ID

        response = self.client.get("/spm/materials/{0}".format(course_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Lesson_Materials_ID": 6,
                "Course_ID": 1,
                "Lesson_Materials": "something"
            }

        })

    def test_update_course(self):
        lm1 = Lesson_Materials(Lesson_Materials_ID=6,
                               Course_ID=1, Lesson_Materials="something")
        db.session.add(lm1)
        db.session.commit()

        course_id = lm1.Course_ID

        response = self.client.get("/spm/materials/{0}".format(course_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Lesson_Materials_ID": 6,
                "Course_ID": 1,
                "Lesson_Materials": "something"
            }
        })


if __name__ == '__main__':
    unittest.main()
