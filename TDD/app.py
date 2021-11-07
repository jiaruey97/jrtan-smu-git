from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg',
                      'gif', 'mp3', 'doc', 'docx', 'pdf', 'ppt', 'pptx'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#### --- CLASSES START --- ####

class Class(db.Model):
    __tablename__ = 'Class'

    Class_ID = db.Column(db.Integer, primary_key=True)
    Class_Name = db.Column(db.String(255), nullable=False)
    Class_Details = db.Column(db.String(255), nullable=False)
    Size = db.Column(db.Integer, nullable=False)
    Current_Size = db.Column(db.Integer)
    Course_ID = db.Column(db.Integer, nullable=False)
    Instructor_ID = db.Column(db.Integer)
    Start_Time = db.Column(db.DateTime, nullable=False)
    End_Time = db.Column(db.DateTime, nullable=False)
    Sections = db.Column(db.Integer, nullable=False)
    Students = db.Column(db.Text)

    def __init__(self, Class_ID, Class_Name, Class_Details, Size, Current_Size, Course_ID,Instructor_ID,Start_Time, End_Time, Sections, Students):
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
        self.Students = Students
        

    def json(self):
        return {"Class_ID": self.Class_ID, "Class_Name": self.Class_Name, "Class_Details": self.Class_Details, "Size": self.Size, "Current_Size": self.Current_Size, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID,"Start_Time": self.Start_Time, "End_Time": self.End_Time, "Sections": self.Sections, "Students": self.Students}

class Course(db.Model):
    __tablename__ = 'Course'

    Course_ID = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(255), nullable=False)
    Course_Details = db.Column(db.String(255), nullable=False)
    Duration = db.Column(db.String(255), nullable=False)
    Prerequisite = db.Column(db.String(255), nullable=False)
    Start_Time = db.Column(db.DateTime, nullable=False)
    End_Time = db.Column(db.DateTime, nullable=False)
    Sections = db.Column(db.Integer, nullable=False)

    def __init__(self, Course_ID, Course_Name, Course_Details, Duration, Prerequisite, Start_Time, End_Time, Sections):
        self.Course_ID = Course_ID
        self.Course_Name = Course_Name
        self.Course_Details = Course_Details
        self.Duration = Duration
        self.Prerequisite = Prerequisite
        self.Start_Time = Start_Time
        self.End_Time = End_Time
        self.Sections = Sections

    def json(self):
        return {"Course_ID": self.Course_ID, "Course_Name": self.Course_Name, "Course_Details": self.Course_Details, "Duration": self.Duration, "Prerequisite": self.Prerequisite, "Start_Time": self.Start_Time, "End_Time": self.End_Time, "Sections": self.Sections}

class Enrollment_Date(db.Model):
    __tablename__ = 'Enrollment_Date'

    Enrollment_ID  = db.Column(db.Integer, primary_key=True)
    Enrollment_Start = db.Column(db.Date)
    Enrollment_End = db.Column(db.Date)


    def __init__(self, Enrollment_ID, Enrollment_Start, Enrollment_End):
        self.Enrollment_ID = Enrollment_ID
        self.Enrollment_Start = Enrollment_Start
        self.Enrollment_End = Enrollment_End
  

    def json(self):
        return {"Enrollment_ID": self.Enrollment_ID, "Enrollment_Start": self.Enrollment_Start, "Enrollment_End": self.Enrollment_End}

class Instructor(db.Model):
    __tablename__ = 'Instructor'

    Instructor_ID = db.Column(db.Integer, primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Username = db.Column(db.String(255), nullable=False)

    def __init__(self, Instructor_ID, Actual_Name,Username):
        self.Instructor_ID = Instructor_ID
        self.Actual_Name = Actual_Name
        self.Username = Username


    def json(self):
        return {"Instructor_ID": self.Instructor_ID, "Actual_Name": self.Actual_Name, "Username": self.Username}

class Lesson_Materials(db.Model):
    __tablename__ = 'Lesson_Materials'

    Lesson_Materials_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer, nullable=False)
    Lesson_Materials = db.Column(db.String(255), nullable=False)

    def __init__(self, Lesson_Materials_ID, Course_ID, Lesson_Materials):
        self.Lesson_Materials_ID = Lesson_Materials_ID
        self.Course_ID = Course_ID
        self.Lesson_Materials = Lesson_Materials

    def json(self):
        return {"Lesson_Materials_ID": self.Lesson_Materials_ID, "Course_ID": self.Course_ID, "Lesson_Materials": self.Lesson_Materials}

class Quiz_Results(db.Model):
    __tablename__ = 'Quiz_Results'

    Quiz_Results_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50))
    Quiz_ID = db.Column(db.Integer)
    Course_ID = db.Column(db.Integer)
    Section = db.Column(db.String(255), nullable=False)
    Marks = db.Column(db.Integer, nullable=False)
    Pass = db.Column(db.Integer, nullable=False)

    def __init__(self, Username, Quiz_ID, Course_ID, Section, Marks, Pass):
        self.Username = Username
        self.Quiz_ID = Quiz_ID
        self.Course_ID = Course_ID
        self.Section = Section
        self.Marks = Marks
        self.Pass = Pass

    def json(self):
        return {"Quiz_Results_ID": self.Quiz_Results_ID, "Username": self.Username, "Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Section": self.Section, "Marks": self.Marks, "Pass": self.Pass}

class Quiz(db.Model):
    __tablename__ = 'Quiz'

    Quiz_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer)
    Instructor_ID = db.Column(db.Integer)
    Section = db.Column(db.String(255), nullable=False)
    Question_Object = db.Column(db.Text, nullable=False)
    Class_ID = db.Column(db.Integer)
    Time = db.Column(db.String(255), nullable=False)


    def __init__(self, Class_ID, Course_ID, Instructor_ID, Section, Question_Object, Time):
        self.Class_ID = Class_ID
        self.Course_ID = Course_ID
        self.Instructor_ID = Instructor_ID
        self.Section = Section
        self.Question_Object = Question_Object
        self.Time = Time


    def json(self):
        return {"Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID, "Section": self.Section, "Question_Object": self.Question_Object, "Class_ID": self.Class_ID, "Time":self.Time}

class Tracker(db.Model):
    __tablename__ = 'Tracker'

    Tracker_ID = db.Column(db.Integer, primary_key=True)
    # Username = db.Column(db.String(50), db.ForeignKey('User_Database.Username'))
    # Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    # Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))
    Username = db.Column(db.String(50))
    Course_ID = db.Column(db.Integer)
    Class_ID = db.Column(db.Integer)
    Sections_cleared = db.Column(db.Integer)
    Quiz_cleared = db.Column(db.Integer)
    Final_Quiz_cleared = db.Column(db.Integer)

    def __init__(self, Username, Course_ID, Class_ID, Sections_cleared, Quiz_cleared, Final_Quiz_cleared):
        #self.Tracker_ID = Tracker_ID
        self.Username = Username
        self.Course_ID = Course_ID
        self.Class_ID = Class_ID
        self.Sections_cleared = Sections_cleared
        self.Quiz_cleared = Quiz_cleared
        self.Final_Quiz_cleared = Final_Quiz_cleared

    def json(self):
        return {"Tracker_ID": self.Tracker_ID, "Username": self.Username, "Course_ID": self.Course_ID, "Class_ID": self.Class_ID, "Sections_cleared": self.Sections_cleared, "Quiz_cleared": self.Quiz_cleared, "Final_Quiz_cleared": self.Final_Quiz_cleared}

class User_Database(db.Model):
    __tablename__ = 'User_Database'

    Username = db.Column(db.String(50), primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    Current_Position = db.Column(db.String(255), nullable=False)
    Course_Assigned = db.Column(db.String(255))
    Course_Completed = db.Column(db.String(255))
    Course_Pending = db.Column(db.String(255))

    def __init__(self, Username, Actual_Name, Department, Current_Position, Course_Assigned, Course_Completed, Course_Pending):
        self.Username = Username
        self.Actual_Name = Actual_Name
        self.Department = Department
        self.Current_Position = Current_Position
        self.Course_Assigned = Course_Assigned
        self.Course_Completed = Course_Completed
        self.Course_Pending = Course_Pending

    def json(self):
        return {"Username": self.Username, "Actual_Name": self.Actual_Name, "Department": self.Department, "Current_Position": self.Current_Position, "Course_Assigned": self.Course_Assigned, "Course_Completed": self.Course_Completed, "Course_Pending": self.Course_Pending}

#### --- CLASS OVER --- ####

### -- Class Methods -- ###

@app.route("/spm/class")
def get_all_class():
    class_list = Class.query.all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "class": [class_in.json() for class_in in class_list]
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

@app.route("/spm/class/<int:Instructor_ID>")
def find_by_instructor_class(Instructor_ID):
    class_list = Class.query.filter_by(Instructor_ID=Instructor_ID).all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "class": [class_i.json() for class_i in class_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Class Not Found not found."
        }
    ), 404

@app.route("/spm/class_id/<int:Class_ID>")
def find_by_class_id(Class_ID):
    class_list = Class.query.filter_by(Class_ID=Class_ID).all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "class": [class_i.json() for class_i in class_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Class Not Found not found."
        }
    ), 404

#Class section update
@app.route("/spm/class/update_section/<int:Course_ID>/<int:section>")
def update_sections_for_course(Course_ID, section):
    class_list = Class.query.filter_by(Course_ID=Course_ID).all()
    if len(class_list):
        for class_item in class_list:
            class_item.Sections = section
            db.session.add(class_item)

    try:
        db.session.commit()
    except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating the sections."
                }
            ), 500 
    
    return jsonify(
        {
            'code': 200,
            "message": "Material update is a success!"
        }
    ), 200



@app.route("/spm/search_class_course/<int:Course_ID>")
def find_by_course_class(Course_ID):
    class_list = Class.query.filter_by(Course_ID=Course_ID).all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "class": [class_i.json() for class_i in class_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Class Not Found not found."
        }
    ), 404

@app.route('/class/<int:Class_ID>/update',methods = ['POST'])
def update_class(Class_ID):
    class_details = Class.query.filter_by(Class_ID=Class_ID)
    if request.method == 'POST':
        if class_details:
            data = request.get_json()
            class_details.update(data)
            db.session.commit()
            return jsonify(
            {
                "code": 200,
                "message": "Update Successful"
            }
        ), 200
    
    return jsonify(
        {
            "code": 404,
            "message": "Oops somethign went wrong"
        }
    ), 404

### -- END Class Methods -- ###

### -- Course Class Methods -- ###

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


@app.route("/spm/course_retrieve/<int:Course_ID>")
def get_course_for_learner(Course_ID):
    course = Course.query.filter_by(Course_ID=Course_ID).one()
    if course != None:
        return jsonify(
            {
                "code": 200,
                "data": course.json()      
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Course Not Found not found."
        }
    ), 404

### -- END Course Class Methods -- ###

## -- Enrollment Date -- ##

@app.route("/spm/enrollment_date")
def get_enrollment_data():
    enrollment_list = Enrollment_Date.query.all()
    if len(enrollment_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "enroll": [enroll.json() for enroll in enrollment_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Enrollment Date."
        }
    ), 404

## --  END Enrollment Date -- ##

## -- Instructor -- ##

@app.route("/spm/instructor")
def get_all_instructor():
    instructor_list = Instructor.query.all()
    if len(instructor_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "instructor": [instructor.json() for instructor in instructor_list]
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

    # Validate User
    user = User_Database.query.filter_by(Username=data['Username']).first()
    if not user:
        return jsonify({
            "code": 500,
            "message": "User not valid."
        }), 500

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

## -- End Instructor -- ##


## -- Materials -- ##

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/spm/materials")
def get_all_materials():
    materia = Lesson_Materials.query.all()
    if len(materia):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "materials": [materials.json() for materials in materia]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no results."
        }
    ), 404


# Retrieve specific material
@app.route("/spm/materials/<int:course_id>")
def get_materials_by_course_id(course_id):
    material = Lesson_Materials.query.filter_by(Course_ID=course_id).one()
    if material:
        return jsonify(
            {
                "code": 200,
                "data": material.json(),
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Material for this course ID cannot be found.",
        }
    ), 404


@app.route("/spm/upload_materials/", methods=['POST'])
def upload_materials_to_server():
    print(request.get_json())
    if 'file' not in request.files:
        return jsonify(
            {
                "code": 500,
                "message": "There are no files uploaded."
            }
        ), 500

    file = request.files['file']

    if file.filename == '':
        return jsonify(
            {
                "code": 500,
                "message": "File name is missing."
            }
        ), 500

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('/opt/bitnami/apache/htdocs/upload/', filename))
        return jsonify(
            {
                "code": 200,
                "message": "File upload is a success"
            }
        )
# This one is only updating/creating new lesson information


@app.route("/update_materials/<int:Lesson_Materials_ID>", methods=['POST'])
def update_materials(Lesson_Materials_ID):
    lesson_materials = Lesson_Materials.query.filter_by(
        Lesson_Materials_ID=Lesson_Materials_ID).first()
    if lesson_materials:
        data = request.get_json()
        print(data)
        print(type(data))
        lesson_materials.Lesson_Materials = json.dumps(data['Lesson_Materials'])

        db.session.add(lesson_materials)
        db.session.commit()

    else:
        data = request.get_json()
        lesson_materials = Lesson_Materials(**data)
        try:
            db.session.add(lesson_materials)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred creating new lesson materials."
                }
            ), 500

    return jsonify(
        {
            'code': 200,
            "message": "It's a success!",
            'data': lesson_materials.json()
        }
    ), 200

## -- End Materials -- ##

## -- Quiz Results -- ##

@app.route("/spm/results")
def get_all_results():
    results = Quiz_Results.query.all()
    if len(results):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quiz_results": [result_i.json() for result_i in results]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no results."
        }
    ), 404

@app.route("/spm/check_if_quiz_completed/<int:quiz_id>/<int:course_id>/<section>/<string:username>")
def check_if_quiz_completed(quiz_id, course_id, section, username):
    result = Quiz_Results.query.filter_by(
        Username=username,
        Quiz_ID=quiz_id,
        Course_ID=course_id,
        Section=section
    ).first()

    if result:
        return jsonify ({
            'code': 200,
            'result': True,
            'section': section,
            'pass': result.json()['Pass'],
            'marks': result.json()['Marks']
        })
    else:
        return jsonify({
            'code': 200,
            'result': False
        })

@app.route("/create_results", methods=['POST'])
def create_results():

    data = request.get_json()
    results = Quiz_Results(Username=data['Username'], Quiz_ID=data['Quiz_ID'], Course_ID=data['Course_ID'], Section=data['Section'], Marks=data['Marks'], Pass=data['Pass'])
    

    # Validate Course
    course = Course.query.filter_by(Course_ID = data['Course_ID']).first()
    if not course:
        return jsonify({
            "code": 500,
            "message": "Course not valid."
        }), 500

    # Validate Quiz
    quiz = Quiz.query.filter_by(Quiz_ID=data['Quiz_ID']).first()
    if not quiz:
        return jsonify({
            "code": 500,
            "message": "Quiz not valid."
        }), 500

    # Validate User_Database
    user = User_Database.query.filter_by(Username=data['Username']).first()
    if not user:
        return jsonify({
            "code": 500,
            "message": "User not valid."
        }), 500

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


## -- End Quiz Results -- ##

## -- Quiz -- ##

@app.route("/spm/quiz")
def get_all_quiz():
    quiz = Quiz.query.all()
    if len(quiz):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quiz": [quiz_i.json() for quiz_i in quiz]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no quiz."
        }
    ), 404

@app.route("/spm/quiz_retrieve/<int:course_id>/<int:class_id>/<section>")
def get_quiz_for_learner(course_id, section, class_id):
    quiz = Quiz.query.filter_by(Course_ID=course_id, Class_ID=class_id, Section=section).first()
    if quiz != None:
        return jsonify(
            {
                "code": 200,
                "data": quiz.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Quiz Not Found not found."
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
                    "quiz": [quiz_i.json() for quiz_i in quiz]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Quiz Not Found not found."
        }
    ), 404


@app.route('/quiz/delete/<int:Quiz_ID>', methods=['POST'])
def delete_quiz(Quiz_ID):
    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID).first()
    if request.method == 'POST':
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            return jsonify(
            {
                "code": 200,
                "message": "Delete Successful"
            }
        ), 200

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

    # Validate Course
    course = Course.query.filter_by(Course_ID=data['Course_ID']).first()
    if not course:
        return jsonify({
            "message": "Course not valid."
        }), 500

    # Validate Instructor
    instructor = Instructor.query.filter_by(Instructor_ID=data['Instructor_ID']).first()
    if not instructor:
        return jsonify({
            "message": "Instructor not valid."
        }), 500

    # Validate Class
    classes = Class.query.filter_by(Class_ID=data['Class_ID']).first()
    if not classes:
        return jsonify({
            "message": "Class not valid."
        }), 500

    quiz = Quiz(**data)

    try:
        db.session.add(quiz)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": quiz.json(),
                "message": "An error occurred creating the Quiz."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": quiz.json()
        }
    ), 201


@app.route('/quiz/<int:Quiz_ID>/update', methods=['POST'])
def update(Quiz_ID):
    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID).first()
    if not quiz:
        return jsonify({
            "code": 500,
            "message": "No Such Quiz Exist!"
    }), 500

    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID)
    if request.method == 'POST':
        if quiz:
            data = request.get_json()
            quiz.update(data)
            db.session.commit()
            return jsonify(
            {
                "code": 200,
                "message": "Update Successful"
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Oops somethign went wrong"
        }
    ), 404

## -- End Quiz -- ##


## -- Tracker -- ##

@app.route("/spm/tracker")
def get_all_tracker():
    tracker = Tracker.query.all()
    if len(tracker):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tracker": [track.json() for track in tracker]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no track."
        }
    ), 404

@app.route("/spm/get_tracker/<string:username>/<int:course_id>/<int:class_id>")
def retrieve_user_tracking_details(username, course_id, class_id):
    tracker = Tracker.query.filter_by(
        Username=username,
        Course_ID=course_id,
        Class_ID=class_id
    ).first()

    if tracker:
        return jsonify(
            {
                "code": 200,
                "data": tracker.json()
            }
        ), 200
    return jsonify(
        {
            {
                "code": 404,
                "message": "Specified tracker cannot be found."
            }
        }
    ), 404


# Initialize the tracker for user
@app.route("/create_tracker/<string:username>/<int:course_id>/<int:class_id>")
def create_tracker(username, course_id, class_id):
    tracker = Tracker(Username=username, Course_ID=course_id,
                      Class_ID=class_id, Sections_clear=0, Quiz_clear=0)
    db.session.add(tracker)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating unique tracking id for user."
            }
        ), 500
    
    return jsonify(
        {
            'code': 200,
            'message': "Unique tracking id created!"
        }
    ), 200

# Instead of JUST updating, we also need to return the tracker to update


@app.route("/spm/update_tracker/<string:username>/<int:course_id>/<int:class_id>/<int:section_number>")
def update_user_section_cleared(username, course_id, class_id, section_number):
    tracker = Tracker.query.filter_by(
        Username=username,
        Course_ID=course_id,
        Class_ID=class_id
    ).first()

    print(tracker.json())
    tracker.Sections_cleared = section_number
    db.session.add(tracker)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "There's an issue updating the tracker with your completed section"
            }
        )

    # Return the section cleared and quiz cleared
    return jsonify(
        {
            "code": 200,
            "data": {
                "Sections_cleared": tracker.Sections_cleared,
                "Quiz_cleared": tracker.Quiz_cleared
            },
            "message": "Section update has been successful"
        }
    )

@app.route("/spm/update_quiz_tracker/<string:username>/<int:course_id>/<int:class_id>")
def update_user_quiz_cleared(username, course_id, class_id):
    tracker = Tracker.query.filter_by(
        Username=username,
        Course_ID=course_id,
        Class_ID=class_id
    ).first()

    tracker.Quiz_cleared += 1
    db.session.add(tracker)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "There's an issue updating the tracker with your completed section"
            }
        )

    # Return the section cleared and quiz cleared
    return jsonify(
        {
            "code": 200,
            "data": {
                "Sections_cleared": tracker.Sections_cleared,
                "Quiz_cleared": tracker.Quiz_cleared
            },
            "message": "Section update has been successful"
        }
    )

@app.route("/spm/update_final_quiz_tracker/<string:username>/<int:course_id>/<int:class_id>/<int:pass_fail>")
def update_user_final_quiz_cleared(username, course_id, class_id, pass_fail):
    tracker = Tracker.query.filter_by(
        Username=username,
        Course_ID=course_id,
        Class_ID=class_id
    ).first()

    #2 means final quiz completed, but user failed
    #1 means final quiz completed, user passed

    if pass_fail == 0:
        tracker.Final_Quiz_cleared = 2
    else:
        tracker.Final_Quiz_cleared = 1

    db.session.add(tracker)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "There's an issue updating the tracker with your completed section"
            }
        )

    # Return the section cleared and quiz cleared
    return jsonify(
        {
            "code": 200,
            "data": {
                "Sections_cleared": tracker.Sections_cleared,
                "Quiz_cleared": tracker.Quiz_cleared
            },
            "message": "Section update has been successful"
        }
    )

## -- End Tracker -- ##

## -- User database -- ##

@app.route("/spm/user_database")
def get_all_user():
    user_Database = User_Database.query.all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


@app.route("/user_database/<string:Username>")
def get_user_name(Username):
    user_Database = User_Database.query.filter_by(Username=Username).all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


@app.route('/user_database/<string:Username>/update', methods=['POST'])
def update_user(Username):
    users = User_Database.query.filter_by(Username=Username)
    if request.method == 'POST':
        if users:
            data = request.get_json()
            users.update(data)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "message": "Update Successful"
                }
            ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Oops somethign went wrong"
        }
    ), 404


@app.route("/user_database/mark_user_course_complete/<string:username>/<int:course_id>/<int:class_id>")
def update_course_completion(username, course_id, class_id):
    user = User_Database.query.filter_by(Username=username).first()
    course_dict = {'course': course_id, 'class': class_id}
    if user:
        #Course assigned
        course_assigned = json.loads(user.json()['Course_Assigned'])
        removed_course_list = []
        removed_course_list[:] = [item for item in course_assigned if item['course'] != course_id and item['class'] != class_id]
        user.Course_Assigned = json.dumps(removed_course_list)

        #Course completed
        new_course_complete = []
        course_completed = user.json()['Course_Completed']

        if course_completed != "":
            new_course_complete.extend(json.loads(course_completed))

        new_course_complete.append(course_dict)
        user.Course_Completed = json.dumps(new_course_complete)

        db.session.add(user)
        db.session.commit()

        try:
            #db.session.commit()
            print('te')
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating for user."
                }
            ), 500

    return jsonify(
        {
            'code': 200,
            'message': "Course completion successfully updated!~"
        }
    ), 200


## -- End userDatabase -- ##
