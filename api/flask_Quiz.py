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


# DATABASE CLASS

class Quiz(db.Model):
    __tablename__ = 'Quiz'

    Quiz_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer)
    Instructor_ID = db.Column(db.Integer)
    Section = db.Column(db.Integer, nullable=False)
    Question_Object = db.Column(db.Text, nullable=False)
    Class_ID = db.Column(db.Integer)


    def __init__(self, Class_ID, Course_ID, Instructor_ID, Section, Question_Object):
        self.Class_ID = Class_ID
        self.Course_ID = Course_ID
        self.Instructor_ID = Instructor_ID
        self.Section = Section
        self.Question_Object = Question_Object


    def json(self):
        return {"Quiz_ID": self.Quiz_ID, "Course_ID": self.Course_ID, "Instructor_ID": self.Instructor_ID, "Section": self.Section, "Question_Object": self.Question_Object, "Class_ID": self.Class_ID}


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
                    "course": [quiz_i.json() for quiz_i in quiz]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no quiz."
        }
    ), 404

@app.route("/spm/quiz_retrieve/<string:Quiz_ID>")
def get_quiz_for_learner(Quiz_ID):
    quiz = Quiz.query.filter_by(Quiz_ID=Quiz_ID).one()
    if len(quiz):
        return jsonify(
            {
                "code": 200,
                "data":{
                    quiz.json()
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Quiz Not Found not found."
        }
    ), 404

#
@app.route("/spm/quiz/<string:Instructor_ID>")
def find_by_isbn13(Instructor_ID):
    quiz = Quiz.query.filter_by(Instructor_ID=Instructor_ID).all()
    if len(quiz):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [quiz_i.json() for quiz_i in quiz]
                }
            }
        )
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
    quiz = Quiz(**data)

    try:
        db.session.add(quiz)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
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

 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5544, debug=True)