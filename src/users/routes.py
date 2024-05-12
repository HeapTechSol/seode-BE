from flask import Blueprint,Flask
from .controller import get_users, add_user, get_user_by_id, delete_user, update_user  # Import get_user_by_id
from flask import jsonify, request
from src.authentication.controller import generate_token

# Define a blueprint for users
user_routes = Blueprint('user_routes', __name__)

# Define routes
user_routes.add_url_rule("/", view_func=get_users, methods=["GET"])  # Get all users
user_routes.add_url_rule("/", view_func=add_user, methods=["POST"])  # Add a new user
user_routes.add_url_rule("/<int:id>", view_func=get_user_by_id, methods=["GET"])  # Get user by ID
user_routes.add_url_rule("/<int:id>", view_func=delete_user, methods=["DELETE"])  # Delete user by ID
user_routes.add_url_rule("/<int:id>", view_func=update_user, methods=["PUT"])  # Update user by ID

# Define the Flask application instance
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(user_routes)
@app.route('/login', methods=['POST'])

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400
    
    access_token = generate_token(email)
    if access_token:
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)