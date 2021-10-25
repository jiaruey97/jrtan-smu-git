from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#local flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spm'

#bitnami flask
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User_Database(db.Model):
    __tablename__ = 'User_Database'

    Username = db.Column(db.String(50), primary_key=True)
    Actual_Name = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    Current_Position = db.Column(db.String(255), nullable=False)
    Course_Assigned = db.Column(db.DateTime, nullable=False)
    Course_Completed = db.Column(db.DateTime, nullable=False)


    def __init__(self, Username, Actual_Name, Department, Current_Position, Course_Assigned, Course_Completed):
        self.Username = Username
        self.Actual_Name = Actual_Name
        self.Department = Department
        self.Current_Position = Current_Position
        self.Course_Assigned = Course_Assigned
        self.Course_Completed = Course_Completed

    def json(self):
        return {"Username": self.Username, "Actual_Name": self.Actual_Name, "Department": self.Department, "Current_Position": self.Current_Position, "Course_Assigned": self.Course_Assigned, "Course_Completed": self.Course_Completed}


@app.route("/spm/user_database")
def get_all_user():
    user_Database = User_Database.query.all()
    if len(user_Database):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": [user.json() for user in user_Database]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5444, debug=True)