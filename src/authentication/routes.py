from flask import Blueprint
from .controller import login, signup

# Define a blueprint for sites
authentication_routes = Blueprint('authentication_routes', __name__)

# Define routes
authentication_routes.add_url_rule("/login", view_func=login, methods=["POST"])
authentication_routes.add_url_rule("/signup", view_func=signup, methods=["POST"])

