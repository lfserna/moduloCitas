from flask import Flask

from app.routes.admin_routes import admin_bp
from app.routes.public_routes import public_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
