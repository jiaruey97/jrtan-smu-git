from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:t2AlF2wAibZH@127.0.0.1:3306/SPM'

@app.route("/testing_hi/helloworld")
def hello_world():
    return 'Hello World'

@app.route("/dynamic_update")
def update_dynamic():
    return 'Checking if dynamic update work!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5245, debug=True)
