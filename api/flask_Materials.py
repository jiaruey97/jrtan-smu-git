from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

#This is the upload path!
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'doc', 'docx', 'pdf', 'ppt', 'pptx'}

#local flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

#bitnami flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Lesson_Materials(db.Model):
    __tablename__ = 'Lesson_Materials'

    Lesson_Materials_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.Integer, db.ForeignKey('Course.Course_ID'))
    Section = db.Column(db.Integer, nullable=False)
    Lesson_Materials = db.Column(db.String(255), nullable=False)


    def __init__(self, Lesson_Materials_ID, Course_ID, Section, Lesson_Materials):
        self.Lesson_Materials_ID = Lesson_Materials_ID
        self.Course_ID = Course_ID
        self.Section = Section
        self.Lesson_Materials = Lesson_Materials

    def json(self):
        return {"Lesson_Materials_ID":self.Lesson_Materials_ID, "Course_ID": self.Course_ID, "Section": self.Section, "Lesson_Materials": self.Lesson_Materials}


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

#Retrieve specific material
@app.route("/spm/materials/<id:course_id>")
def get_materials_by_course_id(course_id):
    material = Lesson_Materials.query.filter_by(Course_id=course_id)
    if len(material):
        return jsonify(
            {
                "code":200,
                "data":{
                    material
                },
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Material for this course ID cannot be found."
        }
    ), 404 

#This one is only updating/creating new lesson information
@app.route("/update_materials/<id:Lesson_Materials_ID>", methods=['POST'])
def update_materials(Lesson_Materials_ID):
    lesson_materials = Lesson_Materials.query.filter_by(Lesson_Materials_ID=Lesson_Materials_ID).first()
    if lesson_materials:
        data = request.get_json()
        lesson_materials.Lesson_Materials = data.Lesson_Materials

        try:
            db.session.commit()
        except:
            {
                "code": 500,
                "message": "An error occurred updating lesson materials."
            }
    else:
        data = request.get_json()
        lesson_materials = Lesson_Materials(**data)

        try:
            db.session.add(lesson_materials)
            db.session.commit()
        except:
            return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating new lesson materials."
            }
        ), 500
    
    return jsonify(
        {
            'code': 201,
            "message": "It's a success!"
        }
    )
    



# @app.route("/create_materials", methods=['POST'])
# def create_materials():

#     data = request.get_json()
#     materials = Lesson_Materials(**data)

#     try:
#         db.session.add(materials)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred creating the materials."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": materials.json()
#         }
#     ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5344, debug=True)