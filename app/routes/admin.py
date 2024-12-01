from flask import Blueprint, jsonify, request
from flask import session
from app.utils import admin_required


admin_blueprint=Blueprint('admin', __name__)

#assuming there can only be one admin
@admin_blueprint.route('/login', methods=['POST'])
def admin_login():
    if session.get('admin'):
        return jsonify({"message" : "Admin already logged in !"}), 200
    
    
    data=request.get_json()
    password=data.get('password')
    if not password:
        return jsonify({"message": "Password is missing"}), 400
    
    if password=="admin":  #the only password can login the admin
        session['admin']=True
        return jsonify({"message" : "Admin logged in"}), 200
    else :
        return jsonify({"message" : "Admin password wrong !"}), 400
    
@admin_blueprint.route('/logout', methods=['GET'])
def admin_logout():
    session.pop('admin', None)
    return jsonify({"message" : "Admin logged out successfully"}), 200


@admin_blueprint.route('/adminonly', methods=['GET'])
@admin_required
def admin_only_endpoint():
    return jsonify({"message": "Admin-only content"})

        
