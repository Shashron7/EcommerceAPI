from flask import Blueprint, jsonify, request
from app import db
from app.models import User
from flask_jwt_extended import create_access_token

users_blueprint=Blueprint('users', __name__)


@users_blueprint.route('/signup', methods=['POST'])
def signup():
    data=request.json
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')


    #querying the User database to see if the email and password are unique are not
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    #creating new user if all goes well
    new_user=User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message ' : 'User created successfully'}), 201


@users_blueprint.route('/login', methods=['POST'])
def login():
    data=request.json
    email=data.get('email')
    password=data.get('password')

    user=User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message' : 'Invalid credentials'}), 401
    
    #Generating JWT token
    access_token=create_access_token(identity={'id' : user.id, 'username' : user.username})

    return jsonify({'access_token': access_token}), 200
    



