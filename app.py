from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from seode.auth.routes import auth_routes
from seode.users.routes import user_routes
from seode.models.config import Config, db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    JWTManager(app) 
    migrate = Migrate(app, db)

    app.register_blueprint(auth_routes, url_prefix="/api/v1/auth")
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")

    with app.app_context():
        db.create_all()

    return app