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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5244, debug=True)