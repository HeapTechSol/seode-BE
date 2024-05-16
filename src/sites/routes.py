from flask import Blueprint
from .controller import get_sites, add_site, get_site_by_id, delete_site, update_site, get_base_urls_of_website

# Define a blueprint for sites
site_routes = Blueprint('site_routes', __name__)

# Define routes
site_routes.add_url_rule("/get-sites", view_func=get_sites, methods=["GET"])
site_routes.add_url_rule("/add-site", view_func=add_site, methods=["POST"])
site_routes.add_url_rule("/<int:id>", view_func=get_site_by_id, methods=["GET"])
site_routes.add_url_rule("/delete/<int:id>", view_func=delete_site, methods=["DELETE"])
site_routes.add_url_rule("/<int:id>", view_func=update_site, methods=["PUT"])
# Define routes
site_routes.add_url_rule("/site", view_func=get_base_urls_of_website, methods=["POST"])