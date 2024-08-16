from flask import Flask, Blueprint
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect() #Ebabke CSRF Protection
    csrf.init_app(app)
    CORS(app)  # Enable CORS for development

    # Import blueprints
    from .routes import routes_blueprint

    app.register_blueprint(routes_blueprint)

    return app

create_app()