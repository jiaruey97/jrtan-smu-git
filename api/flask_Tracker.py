from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

#local flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

#bitnami flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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
                      Class_ID=class_id, Sections_cleared=0, Quiz_cleared=0, Final_Quiz_cleared=0)
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

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5644, debug=True)