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


if __name__ == '__main__':
    app.run(port=5144, debug=True)