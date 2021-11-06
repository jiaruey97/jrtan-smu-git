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
    Username = db.Column(db.String(50))
    Quiz_ID = db.Column(db.Integer)
    Course_ID = db.Column(db.Integer)
    Section = db.Column(db.String(255), nullable=False)
    Marks = db.Column(db.Integer, nullable=False)
    Pass = db.Column(db.Boolean, nullable=False)


    def __init__(self, Username, Quiz_ID, Course_ID, Section, Marks, Pass):
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
    print(data)
    results = Quiz_Results(Username=data['Username'], Quiz_ID=data['Quiz_ID'], Course_ID=data['Course_ID'], Section=data['Section'], Marks=data['Marks'], Pass=data['Pass'])
    db.session.add(results)
    db.session.commit()

    try:
        #db.session.commit()
        print('ge')
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
    app.run(host='0.0.0.0', port=5444, debug=True)