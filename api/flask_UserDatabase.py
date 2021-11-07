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


class User_Database(db.Model):
    __tablename__ = 'User_Database'

    Username = db.Column(db.String(50), primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    Current_Position = db.Column(db.String(255), nullable=False)
    Course_Assigned = db.Column(db.String(255))
    Course_Completed = db.Column(db.String(255))
    Course_Pending = db.Column(db.String(255))

    def __init__(self, Username, Actual_Name, Department, Current_Position, Course_Assigned, Course_Completed, Course_Pending):
        self.Username = Username
        self.Actual_Name = Actual_Name
        self.Department = Department
        self.Current_Position = Current_Position
        self.Course_Assigned = Course_Assigned
        self.Course_Completed = Course_Completed
        self.Course_Pending = Course_Pending

    def json(self):
        return {"Username": self.Username, "Actual_Name": self.Actual_Name, "Department": self.Department, "Current_Position": self.Current_Position, "Course_Assigned": self.Course_Assigned, "Course_Completed": self.Course_Completed, "Course_Pending": self.Course_Pending}


@app.route("/spm/user_database")
def get_all_user():
    user_Database = User_Database.query.all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


@app.route("/user_database/<string:Username>")
def get_user_name(Username):
    user_Database = User_Database.query.filter_by(Username=Username).all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


@app.route('/user_database/<string:Username>/update', methods=['POST'])
def update_user(Username):
    users = User_Database.query.filter_by(Username=Username)
    if request.method == 'POST':
        if users:
            data = request.get_json()
            users.update(data)
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


@app.route("/user_database/mark_user_course_complete/<string:username>/<int:course_id>/<int:class_id>")
def update_course_completion(username, course_id, class_id):
    user = User_Database.query.filter_by(Username=username).first()
    course_dict = {'course': course_id, 'class': class_id}
    if user:
        #Course assigned
        course_assigned = json.loads(user.json()['Course_Assigned'])
        removed_course_list = []
        removed_course_list[:] = [item for item in course_assigned if item['course'] != course_id and item['class'] != class_id]
        user.Course_Assigned = json.dumps(removed_course_list)

        #Course completed
        new_course_complete = []
        course_completed = user.json()['Course_Completed']

        if course_completed != "":
            new_course_complete.extend(json.loads(course_completed))

        new_course_complete.append(course_dict)
        user.Course_Completed = json.dumps(new_course_complete)

        db.session.add(user)
        db.session.commit()

        try:
            #db.session.commit()
            print('te')
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating for user."
                }
            ), 500

    return jsonify(
        {
            'code': 200,
            'message': "Course completion successfully updated!~"
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5744, debug=True)
