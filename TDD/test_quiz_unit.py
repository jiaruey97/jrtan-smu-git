import unittest

from app import Quiz

class TestQuiz(unittest.TestCase):
    def test_to_dict(self):
        q1 = Quiz(Course_ID=1, Instructor_ID = 1, 
                Section="1", Question_Object='Chickensds', Class_ID=1,
                Time="23")
        self.assertEqual(q1.json(), {
            "Quiz_ID": None,
            "Course_ID":1,
            "Instructor_ID":1,
            "Section":"1",
            "Question_Object":"Chickensds",
            "Class_ID": 1,
            "Time": "23"
        }
        )

        
        

if __name__ == "__main__":
    unittest.main()