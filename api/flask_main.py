from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:8889/spm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# DATABASE CLASS

class Course(db.Model):
    __tablename__ = 'Course'

    Course_ID = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(255), nullable=False)
    Course_Details = db.Column(db.String(255), nullable=False)
    Duration = db.Column(db.String(255), nullable=False)
    Prerequestic = db.Column(db.String(255), nullable=False)
    Start_Time = db.Column(db.DateTime, nullable=False)
    End_Time = db.Column(db.DateTime, nullable=False)
    Sections = db.Column(db.Integer, nullable=False)

    def __init__(self, Course_ID, Course_Name, Course_Details, Duration, Prerequestic, Start_Time, End_Time, Sections):
        self.Course_ID = Course_ID
        self.Course_Name = Course_Name
        self.Course_Details = Course_Details
        self.Duration = Duration
        self.Prerequestic = Prerequestic
        self.Start_Time = Start_Time
        self.End_Time = End_Time
        self.Sections = Sections

    def json(self):
        return {"Course_ID": self.Course_ID, "Course_Name": self.Course_Name, "Course_Details": self.Course_Details, "Duration": self.Duration, "Prerequestic": self.Prerequestic, "Start_Time": self.Start_Time, "End_Time": self.End_Time, "Sections": self.Sections}

class Class(db.Model):
    __tablename__ = 'Class'

    Class_ID = db.Column(db.Integer, primary_key=True)
    Class_Name = db.Column(db.String(255), nullable=False)
    Class_Details = db.Column(db.String(255), nullable=False)
    Size = db.Column(db.Integer, nullable=False)
    Current_Size = db.Column(db.Integer)
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Instructor_ID = db.Column(db.Integer)
    Start_Time = db.Column(db.DateTime, nullable=False)
    End_Time = db.Column(db.DateTime, nullable=False)
    Sections = db.Column(db.Integer, db.ForeignKey('Course.Sections'))


    def __init__(self, Class_ID, Class_Name, Class_Details, Size, Current_Size, Course_ID,Instructor_ID,Start_Time, End_Time, Sections):
        self.Class_ID = Class_ID
        self.Class_Name = Class_Name
        self.Class_Details = Class_Details
        self.Size = Size
        self.Current_Size = Current_Size
        self.Course_ID = Course_ID
        self.Instructor_ID = Instructor_ID
        self.Start_Time = Start_Time
        self.End_Time = End_Time
        self.Sections = Sections
        

    def json(self):
        return {"Class_ID": self.Class_ID, "Class_Name": self.Class_Name, "Class_Details": self.Class_Details, "Size": self.Size, "Current_Size": self.Current_Size, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID,"Start_Time": self.Start_Time, "End_Time": self.End_Time, "Sections": self.Sections}


class Instructor(db.Model):
    __tablename__ = 'Instructor'

    Instructor_ID = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)


    def __init__(self, Instructor_ID, LastName, FirstName):
        self.Instructor_ID = Instructor_ID
        self.LastName = LastName
        self.FirstName = FirstName


    def json(self):
        return {"Instructor_ID": self.Instructor_ID, "LastName": self.LastName, "FirstName": self.FirstName}


class User_Database(db.Model):
    __tablename__ = 'User_Database'

    Username = db.Column(db.String(50), primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Designation = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    Current_Role = db.Column(db.String(255), nullable=False)
    Course_Assigned = db.Column(db.DateTime, nullable=False)
    Course_Completed = db.Column(db.DateTime, nullable=False)


    def __init__(self, Username, Actual_Name, Designation, Department, Current_Role, Course_Assigned, Course_Completed):
        self.Username = Username
        self.Actual_Name = Actual_Name
        self.Designation = Designation
        self.Department = Department
        self.Current_Role = Current_Role
        self.Course_Assigned = Course_Assigned
        self.Course_Completed = Course_Completed

    def json(self):
        return {"Username": self.Username, "Actual_Name": self.Actual_Name, "Designation": self.Designation,"Department": self.Department, "Current_Role": self.Current_Role, "Course_Assigned": self.Course_Assigned, "Course_Completed": self.Course_Completed}

class Quiz(db.Model):
    __tablename__ = 'Quiz'

    Quiz_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Instructor_ID = db.Column(db.Integer, db.ForeignKey('Instructor.Instructor_ID'))
    Section = db.Column(db.Integer, nullable=False)
    Question_Object = db.Column(db.String(255), nullable=False)
    Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))



    def __init__(self, Class_ID, Course_ID, Instructor_ID, Section, Question_Object):
        self.Class_ID = Class_ID
        self.Course_ID = Course_ID
        self.Instructor_ID = Instructor_ID
        self.Section = Section
        self.Question_Object = Question_Object


    def json(self):
        return {"Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID, "Section": self.Section, "Question_Object": self.Question_Object, "Class_ID": self.Class_ID}


class Quiz_Results(db.Model):
    __tablename__ = 'Quiz_Results'

    Quiz_Results_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), db.ForeignKey('User_Database.Username'))
    Quiz_ID = db.Column(db.Integer, db.ForeignKey('Quiz.Quiz'))
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Section = db.Column(db.Integer, nullable=False)
    Marks = db.Column(db.Integer, nullable=False)
    Pass = db.Column(db.Boolean, nullable=False)


    def __init__(self,  Quiz_Results_ID, Username, Quiz_ID, Course_ID, Section, Marks, Pass):
        self.Quiz_Results_ID = Quiz_Results_ID
        self.Username = Username
        self.Quiz_ID = Quiz_ID
        self.Course_ID = Course_ID
        self.Section = Section
        self.Marks = Marks
        self.Pass = Pass

    def json(self):
        return {"Quiz_Results_ID": self.Quiz_Results_ID, "Username": self.Username, "Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Section": self.Section, "Marks": self.Marks, "Pass": self.Pass}

class Tracker(db.Model):
    __tablename__ = 'Tracker'

    Tracker_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), db.ForeignKey('User_Database.Username'))
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))
    Section_Object = db.Column(db.String(255), nullable=False)


    def __init__(self, Tracker_ID, Username, Course_ID, Class_ID, Section_Object):
        self.Tracker_ID = Tracker_ID
        self.Username = Username
        self.Course_ID = Course_ID
        self.Class_ID = Class_ID
        self.Section_Object = Section_Object

    def json(self):
        return {"Tracker_ID": self.Tracker_ID, "Username": self.Username, "Course_ID": self.Course_ID, "Class_ID": self.Class_ID, "Section_Object": self.Section_Object}

class Lesson_Materials(db.Model):
    __tablename__ = 'Lesson_Materials'

    Lesson_Materials_ID = db.Column(db.Integer, primary_key=True)
    Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))
    Section = db.Column(db.Integer, nullable=False)
    Lesson_Materials = db.Column(db.String(255), nullable=False)


    def __init__(self, Lesson_Materials_ID, Class_ID, Section, Lesson_Materials):
        self.Lesson_Materials_ID = Lesson_Materials_ID
        self.Class_ID = Class_ID
        self.Section = Section
        self.Lesson_Materials = Lesson_Materials

    def json(self):
        return {"Lesson_Materials_ID":self.Lesson_Materials_ID, "Class_ID": self.Class_ID, "Section": self.Section, "Lesson_Materials": self.Lesson_Materials}

###################################################################################################################################################################################################################
#FLASK METHODS below

# Course Methods

@app.route("/spm/course")
def get_all_course():
    course_list = Course.query.all()
    if len(course_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [course.json() for course in course_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no courses."
        }
    ), 404

#No Create Course Methods as it is assume to be completed

# Class Methods

@app.route("/spm/class")
def get_all_class():
    class_list = Class.query.all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [class_in.json() for class_in in class_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no class."
        }
    ), 404

@app.route("/create_class", methods=['POST'])
def create_class():

    data = request.get_json()
    results = Class(**data)

    try:
        db.session.add(results)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Class."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": results.json()
        }
    ), 201

@app.route("/spm/class/<string:Instructor_ID>")
def find_by_instructor_class(Instructor_ID):
    class_list = Class.query.filter_by(Instructor_ID=Instructor_ID).all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [class_i.json() for class_i in class_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Class Not Found not found."
        }
    ), 404

#Instructor Methods

@app.route("/spm/instructor")
def get_all_instructor():
    instructor_list = Instructor.query.all()
    if len(instructor_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [instructor.json() for instructor in instructor_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no instructor."
        }
    ), 404

@app.route("/create_instructor", methods=['POST'])
def create_instructor():

    data = request.get_json()
    results = Instructor(**data)

    try:
        db.session.add(results)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Instructor."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": results.json()
        }
    ), 201


#User Database Methods

@app.route("/spm/user_database")
def get_all_user():
    user_Database = User_Database.query.all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

#No Create USER DATABASE, it is assume to be Populated.


# RESULTS METHOD

@app.route("/spm/results")
def get_all_results():
    results = Quiz_Results.query.all()
    if len(results):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [result_i.json() for result_i in results]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no results."
        }
    ), 404

@app.route("/create_results", methods=['POST'])
def create_results():

    data = request.get_json()
    results = Quiz_Results(**data)

    try:
        db.session.add(results)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the results."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": results.json()
        }
    ), 201

# LESSON MATERIAL METHODS

@app.route("/spm/tracker")
def get_all_tracker():
    tracker = Tracker.query.all()
    if len(tracker):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [track.json() for track in tracker]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no track."
        }
    ), 404

@app.route("/create_tracker", methods=['POST'])
def create_tracker():

    data = request.get_json()
    tracker = Tracker(**data)

    try:
        db.session.add(tracker)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the tracker."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tracker.json()
        }
    ), 201


# LESSON MATERIAL METHODS 

@app.route("/spm/materials")
def get_all_materials():
    materia = Lesson_Materials.query.all()
    if len(materia):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [materials.json() for materials in materia]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no results."
        }
    ), 404


@app.route("/create_materials", methods=['POST'])
def create_materials():

    data = request.get_json()
    materials = Lesson_Materials(**data)

    try:
        db.session.add(materials)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the materials."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": materials.json()
        }
    ), 201



# QUIZ METHODS

#Retrieve all Quiz
@app.route("/spm/quiz")
def get_all_quiz():
    quiz = Quiz.query.all()
    if len(quiz):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [quiz_i.json() for quiz_i in quiz]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no quiz."
        }
    ), 404

#
@app.route("/spm/quiz/<string:Instructor_ID>")
def find_by_isbn13(Instructor_ID):
    quiz = Quiz.query.filter_by(Instructor_ID=Instructor_ID).all()
    if len(quiz):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [quiz_i.json() for quiz_i in quiz]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Quiz Not Found not found."
        }
    ), 404

@app.route('/quiz/delete/<int:Quiz_ID>', methods=['DELETE'])
def delete_quiz(Quiz_ID):
    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID).delete()
    if quiz:
        return jsonify(
            {
                "code": 200,
                "message": "We have successfully Delete the Quiz."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Oops somethign went wrong"
        }
    ), 404
    

# Create Quiz
@app.route("/create_quiz", methods=['POST'])
def create_quiz():

    data = request.get_json()
    quiz = Quiz(**data)

    try:
        db.session.add(quiz)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Quiz."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": quiz.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(port=5000, debug=True)