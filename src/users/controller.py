from flask import jsonify, request
from db import get_connection, release_connection
from src.authentication.controller import hash_password, check_password  # Import authentication functions

# Import queries from queries.py
from .queries import get_users_query, get_user_by_id_query, check_email_exists_query, \
                      add_user_query, delete_user_query, update_user_query

# Function to get all users
def get_users():
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_users_query)
                users = cur.fetchall()
                return jsonify(users), 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to get a user by ID
def get_user_by_id(id):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_user_by_id_query, (id,))
                user = cur.fetchone()
                if user:
                    return jsonify(user), 200
                return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to authenticate and get user by email and password
def authenticate_user(email, password):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(check_email_exists_query, (email,))
                user = cur.fetchone()
                if user:
                    hashed_password = user['password']
                    if check_password(password, hashed_password):
                        return jsonify({"message": "Authentication successful"}), 200
                    else:
                        return jsonify({"message": "Incorrect password"}), 401
                return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to add a new user
def add_user():
    try:
        data = request.json
        firstname, lastname, email, password = data['firstname'], data['lastname'], data['email'], data['password']
        password = hash_password(password)  # Hash the password before storing
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                # cur.execute(check_email_exists_query, (email,))
                if cur.rowcount > 0:
                    return "Email already exists.", 400
                cur.execute(add_user_query, (firstname, lastname, email, password))
                conn.commit()
                return "User created successfully!", 201
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            release_connection(conn)

# Function to delete a user
def delete_user(id):
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_user_by_id_query, (id,))
                if not cur.fetchone():
                    return "User does not exist in the database", 404
                cur.execute(delete_user_query, (id,))
                conn.commit()
                return "User deleted successfully.", 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)

# Function to update a user
def update_user(id):
    try:
        data = request.json
        firstname, lastname, email, password = data['firstname'], data['lastname'], data['email'], data['password']
        password = hash_password(password)  # Hash the password before updating
        conn = get_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(get_user_by_id_query, (id,))
                if not cur.fetchone():
                    return "User does not exist in the database", 404
                cur.execute(update_user_query, (firstname, lastname, email, password, id))
                conn.commit()
                return "User updated successfully.", 200
        return jsonify({"message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        release_connection(conn)