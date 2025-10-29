# app/__init__.py
from flask import Flask, app
from flask_cors import CORS
from flask_migrate import Migrate
from app.db import db
from app.config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    # Import and register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.caregiver_routes import caregiver_bp
    from app.routes.emergency_routes import emergency_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(caregiver_bp, url_prefix="/api/caregiver")
    app.register_blueprint(emergency_bp, url_prefix="/api/emergency")

# Basic route to check if the app is running
    @app.route("/")
    def index():
        return {"message": "MediChain backend is up"}

    return app
