from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token

from seode.models.config import db
from seode.models.users import User

@jwt_required()
def get_users():
    all_users = User.query.all()
    user_dict = [user.to_dict(rules=('-password_hash',)) for user in all_users]
    return jsonify({"message": "", "result":user_dict}), 200