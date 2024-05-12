from flask import jsonify, request
from db import get_connection, release_connection
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask import jsonify
from flask_jwt_extended import create_access_token
from src.users.queries import check_email_exists_query, add_user_query


def hash_password(password):
    """
    Hashes the given password using bcrypt.
    """
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    """
    Checks if the given password matches the hashed password.
    Returns True if the passwords match, False otherwise.
    """
    # Encode the password and hashed_password to bytes
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # Use bcrypt to check if the password matches the hashed password
    is_matched = bcrypt.checkpw(password_bytes, hashed_password_bytes)
    return is_matched

def authenticate(email, password):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(check_email_exists_query, (email,))
                user = cur.fetchone()
                if user and check_password(password, user[-1]):
                    return user
        return None
    except Exception as e:
        return None
    finally:
        release_connection(conn)

def init_app(app):
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    jwt = JWTManager(app)

def generate_token(email, password):
    user = authenticate(email, password)
    if user:
        access_token = create_access_token(identity=user[0])  # You can customize the token as needed
        return {'access_token':access_token, 'firstname':user[1], 'lastname':user[2], 'email':user[3]}
    else:
        return None

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400
    
    access_token = generate_token(email, password)
    if access_token:
        return jsonify(access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


def create_user(firstname, lastname, email, password):
    try:
        password = hash_password(password)
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(check_email_exists_query, (email,))
                if cur.rowcount > 0:
                    return jsonify({"message": "Email already exists."}), 400
                cur.execute(add_user_query, (firstname, lastname, email, password))
                conn.commit()
                return jsonify({"message": "User signed up successfully"}), 201
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            release_connection(conn)
    
def signup():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    # Validate user input (e.g., check for missing fields)
    if not firstname or not lastname or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if the user already exists (optional, depending on your application logic)

    # Add the user to the database
    result = create_user(firstname, lastname, email, password)
    return result