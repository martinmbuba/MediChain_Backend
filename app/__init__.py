# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .db import db
from .config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Import models so Flask-Migrate can detect them
    from app import models

    # ✅ Import and register routes
    from .routes import register_routes
    register_routes(app)


    # Simple test route
    @app.route('/')
    def index():
        return {"message": "MediChain backend is up"}

    return app
