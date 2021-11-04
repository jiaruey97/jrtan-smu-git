from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# local flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

# bitnami flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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


@app.route("/spm/enrollment_date")
def get_all_course():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5944, debug=True)
