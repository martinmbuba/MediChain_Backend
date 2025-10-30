import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,  # Adjust based on Supabase limits
    host="aws-1-eu-west-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
    user="postgres.kmpzmzneqmkhvgedkzcp",
    password="MartinMbuba2552.",
    cursor_factory=RealDictCursor
)

def get_db_connection():
    return connection_pool.getconn()

def release_db_connection(conn):
    connection_pool.putconn(conn)
