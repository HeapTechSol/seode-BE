from flask import Blueprint

from .controller import get_users

user_routes = Blueprint('user_routes', __name__)

user_routes.add_url_rule("/list", view_func=get_users, methods=["GET"])