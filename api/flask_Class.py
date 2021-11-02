

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#local flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

#bitnami flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route("/spm/search_class_course/<int:Course_ID>")
def find_by_course_class(Course_ID):
    class_list = Class.query.filter_by(Course_ID=Course_ID).all()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5044, debug=True)