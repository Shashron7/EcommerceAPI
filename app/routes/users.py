from flask import Blueprint, jsonify, request
from app import db
from app.models import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import session
from app.utils import login_required

users_blueprint=Blueprint('users', __name__)


@users_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 409

    # Create a new user
    new_user = User(username=username, email=email, password=password)  # Hash password in real scenarios
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@users_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Find user in the database
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:  
        return jsonify({"error": "Invalid username or password"}), 401

    # Create a session
    session['user_id'] = user.id  # Store user ID in the session
    return jsonify({"message": "Login successful"}), 200




@users_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clears all session data
    return jsonify(message="Logged out successfully"), 200



@users_blueprint.route('/wallet', methods=['GET'])
@login_required
def view_wallet():
    user_id=session['user_id']
    user=User.query.get(user_id)
    if not user:
        return jsonify({"Message" : "User not found"}), 404
    
    return jsonify({"Wallet_Balance" : user.wallet_balance}), 200



@users_blueprint.route('/wallet/add', methods=['POST'])
@login_required
def add_balance():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    amount = data.get('amount', 0)

    if amount <= 0:
        return jsonify({"message": "Invalid amount"}), 400

    if user.wallet_balance is None:
        user.wallet_balance=0.0
    user.wallet_balance += amount
    db.session.commit()

    return jsonify({"message": "Balance updated", "wallet_balance": user.wallet_balance}), 200
