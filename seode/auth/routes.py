from flask import Blueprint

from .controller import signup, login

auth_routes = Blueprint('auth_routes', __name__)

auth_routes.add_url_rule("/login", view_func=login, methods=["POST"])
auth_routes.add_url_rule("/signup", view_func=signup, methods=["POST"])