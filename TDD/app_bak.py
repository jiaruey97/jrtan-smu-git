from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#local flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

#bitnami flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    if course is not None:
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


class Class(db.Model):
    __tablename__ = 'Class'

    Class_ID = db.Column(db.Integer, primary_key=True)
    Class_Name = db.Column(db.String(255), nullable=False)
    Class_Details = db.Column(db.Text, nullable=False)
    Size = db.Column(db.Integer, nullable=False)
    Current_Size = db.Column(db.Integer, nullable=False)
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Instructor_ID = db.Column(db.Integer, nullable=False)
    Start_Time = db.Column(db.DateTime, nullable=False)
    End_Time = db.Column(db.DateTime, nullable=False)
    Sections = db.Column(db.Integer, nullable=False)
    Students = db.Column(db.Text, nullable=False)

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

    # Validate Course
    course = Course.query.filter_by(Course_ID = data['Course_ID']).first()
    if not course:
        return jsonify({
            "code": 500,
            "message": "Course not valid."
        }), 500

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

#Class section update
@app.route("/spm/class/update_section/<int:Course_ID>/<int:section>")
def update_sections_for_course(Course_ID,section):
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


@app.route("/spm/search_class/<int:Class_ID>")
def find_by_class(Class_ID):
    class_list = Class.query.filter_by(Class_ID=Class_ID).all()
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

class User_Database(db.Model):
    __tablename__ = 'User_Database'

    Username = db.Column(db.String(50), primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    Current_Position = db.Column(db.String(255), nullable=False)
    Course_Assigned = db.Column(db.String(255), nullable=False)
    Course_Completed = db.Column(db.String(255), nullable=False)
    Course_Pending = db.Column(db.String(255), nullable=False)


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


@app.route('/user_database/<string:Username>/update',methods = ['POST'])
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


class Instructor(db.Model):
    __tablename__ = 'Instructor'

    Instructor_ID = db.Column(db.Integer, primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Username = db.Column(db.String(255), db.ForeignKey('User_Database.Username'))

    def __init__(self, Instructor_ID, Actual_Name, Username):
        self.Instructor_ID = Instructor_ID
        self.Actual_Name = Actual_Name
        self.Username = Username


    def json(self):
        return {"Instructor_ID": self.Instructor_ID, "Actual_Name": self.Actual_Name, "Username": self.Username}



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

# This function checks if files are allowed


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
            "message": "Material for this course ID cannot be found."
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
        Lesson_Materials_ID=Lesson_Materials_ID).one()
    if lesson_materials:
        data = request.get_json()
        print(data)
        print(data['Lesson_Materials'])
        print(lesson_materials)
        lesson_materials.Lesson_Materials = json.dumps(
            data['Lesson_Materials'])
        print(lesson_materials.Lesson_Materials)
        db.session.add(lesson_materials)
        db.session.commit()
        # try:
        #      db.session.add(lesson_materials)
        #      db.session.commit()
        # except:
        #     {
        #         "code": 500,
        #         "message": "An error occurred updating lesson materials."
        #     }
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
            "message": "It's a success!"
        }
    ), 200

class Quiz(db.Model):
    __tablename__ = 'Quiz'

    Quiz_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Instructor_ID = db.Column(db.Integer, db.ForeignKey('Instructor.Instructor_ID'))
    Section = db.Column(db.String(255), nullable=False)
    Question_Object = db.Column(db.Text, nullable=False)
    Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))
    Timing = db.Column(db.String(255), nullable=False)


    def __init__(self, Class_ID, Course_ID, Instructor_ID, Section, Question_Object, Timing):
        self.Class_ID = Class_ID
        self.Course_ID = Course_ID
        self.Instructor_ID = Instructor_ID
        self.Section = Section
        self.Question_Object = Question_Object
        self.Timing = Timing


    def json(self):
        return {"Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID, "Section": self.Section, "Question_Object": self.Question_Object, "Class_ID": self.Class_ID, "Timing":self.Timing}


###################################################################################################################################################################################################################
#FLASK METHODS below

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

@app.route("/spm/quiz_retrieve/<int:Quiz_ID>")
def get_quiz_for_learner(Quiz_ID):
    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID).first()
    if quiz is not None:
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
@app.route("/spm/quiz/<int:Instructor_ID>")
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
        ), 200
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
    course = Course.query.filter_by(Course_ID = data['Course_ID']).first()
    if not course:
        return jsonify({
            "code": 500,
            "message": "Course not valid."
        }), 500

    # Validate Instructor
    instructor = Instructor.query.filter_by(Instructor_ID=data['Instructor_ID']).first()
    if not instructor:
        return jsonify({
            "code": 500,
            "message": "Instructor not valid."
        }), 500

    # Validate Class
    classes = Class.query.filter_by(Class_ID=data['Class_ID']).first()
    if not classes:
        return jsonify({
            "code": 500,
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

@app.route('/quiz/<int:Quiz_ID>/update',methods = ['POST'])
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


class Quiz_Results(db.Model):
    __tablename__ = 'Quiz_Results'

    Quiz_Results_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), db.ForeignKey('User_Database.Username'))
    Quiz_ID = db.Column(db.Integer, db.ForeignKey('Quiz.Quiz_ID'))
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

@app.route("/spm/results")
def get_all_results():
    results = Quiz_Results.query.all()
    if len(results):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "results": [result_i.json() for result_i in results]
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

@app.route("/spm/get_tracker/<string:username>")
def retrieve_user_track():
    data = request.get_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5044, debug=True)