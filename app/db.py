import psycopg2
from psycopg2.extras import RealDictCursor
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def get_db_connection():
    return psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
