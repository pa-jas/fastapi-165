"""Database configuration and connection"""
from sqlalchemy import create_engine

# Database connection URL
DB_ENGINE_URL = "postgresql+psycopg://pa_jas:P*ssw0rd_PA@103.59.160.166:5432/dwh"

# Create SQLAlchemy engine
engine = create_engine(
    DB_ENGINE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for SQL query logging
)
