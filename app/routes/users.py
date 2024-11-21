from flask import Blueprint, jsonify

users_blueprint=Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['POST'])
def register_user():
    return jsonify({"message" : "User registered"})


