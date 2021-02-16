from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder.models.mixins import ImageColumn

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/flasK_task/flsk.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    profile_picture = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))
    addresses = db.relationship('Address', backref='user', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat = db.Column(db.String(120))
    address_line_1 = db.Column(db.String(120))
    address_line_2 = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    pincode = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/user', methods=['GET'])
def get_all_users(current_user): # For getting list of all user's
    users = User.query.all()
    output = []
    for user in users:
        user_data = {} # Data formation in dictionary
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['phone'] = user.phone
        user_data['profile_picture'] = user.profile_picture
        user_data['addresses'] = user.addresses
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(current_user, public_id): # For getting single user's

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {} # Data formation in dictionary
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['email'] = user.email
    user_data['phone'] = user.phone
    user_data['profile_picture'] = user.profile_picture
    user_data['addresses'] = user.addresses

    return jsonify({'user' : user_data})

if __name__ == '__main__':
    app.run(debug=True)