from flask import request, jsonify
from flask_jwt_extended import create_access_token

from seode.models.config import db
from seode.models.users import User

def signup():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(firstName=firstName, lastName=lastName, email=email, password=password)
    new_user.set_password(password)  

    try:
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        user_dict = new_user.to_dict(rules=('-password_hash',))
        return jsonify({"message": "User created successfully", "result":{ "access_token": access_token, "user":user_dict}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to create user", "error": str(e)}), 500


def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        user_dict = user.to_dict(rules=('-password_hash',))
        return jsonify({"message": "Login successful", "result":{ "access_token": access_token, "user":user_dict}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
