from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# local flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

# bitnami flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tracker(db.Model):
    __tablename__ = 'Tracker'

    Tracker_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50))
    Course_ID = db.Column(db.Integer)
    Class_ID = db.Column(db.Integer)
    Section_Object = db.Column(db.Text)

    def __init__(self, Username, Course_ID, Class_ID, Section_Object):
        #self.Tracker_ID = Tracker_ID
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
    print(tracker.json())
    print(tracker.json()["Section_Object"])
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

{"sections_cleared": 0, "quiz_cleared": 0}
# Initialize the tracker for user


@app.route("/create_tracker/<string:username>/<int:course_id>/<int:class_id>")
def create_tracker(username, course_id, class_id):
    json_track = json.dumps({'sections_cleared': 0, 'quiz_cleared': 0})
    tracker = Tracker(Username=username, Course_ID=course_id,
                      Class_ID=class_id, Section_Object=json_track)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5644, debug=True)
