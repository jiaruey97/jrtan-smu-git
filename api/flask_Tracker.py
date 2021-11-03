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

@app.route("/spm/get_tracker/<string:username>")
def retrieve_user_track():
    data = request.get_json()
    

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5644, debug=True)