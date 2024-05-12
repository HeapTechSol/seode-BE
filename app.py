from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
#from auth import init_app as init_auth
from src.users.routes import user_routes
from src.sites.routes import site_routes  # Import the Blueprint for sites routes
from src.authentication.routes import authentication_routes  # Import the Blueprint for sites routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key' 
jwt = JWTManager(app)
#init_auth(app)
CORS(app)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    return jsonify({"message": "This route is protected"}), 200

@app.route("/")
def hello():
    return "Hello World!"

app.register_blueprint(user_routes, url_prefix="/api/v1/users")
app.register_blueprint(site_routes, url_prefix="/api/v1/sites")  # Register the sites routes
app.register_blueprint(authentication_routes, url_prefix="/api/v1/auth")  # Register the sites routes

if __name__ == "__main__":
    app.run(port=3000)
