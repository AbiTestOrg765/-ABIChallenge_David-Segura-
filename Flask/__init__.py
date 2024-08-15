from flask import Flask, Blueprint
from flask_cors import CORS
import logging
def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for development

    # Import blueprints or other components here
    from .routes import routes_blueprint

    app.register_blueprint(routes_blueprint)

    return app

create_app()