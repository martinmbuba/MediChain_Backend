# app/__init__.py
from flask import Flask
from flask_cors import CORS
from .db import db
from .config import Config
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register_routes(app)

    @app.route('/')
    def index():
        return {"message": "MediChain backend is up"}

    return app

