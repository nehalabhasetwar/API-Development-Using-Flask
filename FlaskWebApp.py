from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy    #ORM to communicate with the database without writing SQL
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api    #Extension of the Flask library which Enables us to develop APIs quickly

# Connect to Database and create database session
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Declare a model for Students
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email_id = db.Column(db.String(32))
    contest_rank=db.Column(db.Integer)

    def __init__(self, username, first_name, last_name, email_id,contest_rank):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email_id = email_id
        self.contest_rank=contest_rank

# Declare a schema for Students. It is class that inherits from Marshmallow.Schema,
# and is used to avoid the headache of JSON parsing.
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email_id','contest_rank')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# We will now proceed with the actual API development.
# Complete logic is written in a single class, called UserManager


# Here in GET method, we will fetch all students data
@app.route("/student", methods=["GET"])
def get():
    try:
        id = request.args['id']
    except Exception as _:
        id = None

    if not id:
        users = Student.query.all()
        return jsonify(users_schema.dump(users))
    user = Student.query.get(id)
    return jsonify(user_schema.dump(user))

# Here in POST method, we will insert new Student into our database
@app.route("/student", methods=["POST"])
def post():
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email_id = request.json['email_id']
    contest_rank = request.json['contest_rank']

    user = Student(username, first_name, last_name, email_id,contest_rank)
    db.session.add(user)
    db.session.commit()

    return jsonify({
            'Message': f'User {first_name} {last_name} inserted.'
        })

# Here in PUT method, we will update data of existing Student from our database
@app.route("/student", methods=["PUT"])
def put():
    try:
        id = request.args['id']
    except Exception as _:
        id = None

    if not id:
        return jsonify({'Message': 'Must provide the user ID'})

    user = Student.query.get(id)
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email_id = request.json['email_id']
    contest_rank = request.json['contest_rank']

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email_id = email_id
    user.contest_rank = contest_rank

    db.session.commit()

    return jsonify({
            'Message': f'User {first_name} {last_name} altered.'
        })

# Here in delete method, we will delete data of existing Student from our database
@app.route("/student", methods=["DELETE"])
def delete():
    try:
        id = request.args['id']
    except Exception as _:
        id = None

    if not id:
        return jsonify({'Message': 'Must provide the user ID'})

    user = Student.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({
            'Message': f'User {str(id)} deleted.'
        })


if __name__ == '__main__':
    app.run(debug=True)

#The API is now running at http://127.0.0.1:5000/api/student