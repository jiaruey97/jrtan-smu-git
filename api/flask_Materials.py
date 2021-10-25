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

class Lesson_Materials(db.Model):
    __tablename__ = 'Lesson_Materials'

    Lesson_Materials_ID = db.Column(db.Integer, primary_key=True)
    Class_ID = db.Column(db.Integer, db.ForeignKey('Class.Class_ID'))
    Section = db.Column(db.Integer, nullable=False)
    Lesson_Materials = db.Column(db.String(255), nullable=False)


    def __init__(self, Lesson_Materials_ID, Class_ID, Section, Lesson_Materials):
        self.Lesson_Materials_ID = Lesson_Materials_ID
        self.Class_ID = Class_ID
        self.Section = Section
        self.Lesson_Materials = Lesson_Materials

    def json(self):
        return {"Lesson_Materials_ID":self.Lesson_Materials_ID, "Class_ID": self.Class_ID, "Section": self.Section, "Lesson_Materials": self.Lesson_Materials}


@app.route("/spm/materials")
def get_all_materials():
    materia = Lesson_Materials.query.all()
    if len(materia):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [materials.json() for materials in materia]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no results."
        }
    ), 404


@app.route("/create_materials", methods=['POST'])
def create_materials():

    data = request.get_json()
    materials = Lesson_Materials(**data)

    try:
        db.session.add(materials)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the materials."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": materials.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5344, debug=True)