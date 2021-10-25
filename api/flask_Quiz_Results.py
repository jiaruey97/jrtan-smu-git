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

if __name__ == '__main__':
    app.run(port=5544, debug=True)