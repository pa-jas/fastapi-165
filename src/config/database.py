"""Database configuration and connection"""
import os

from sqlalchemy import create_engine

# Database connection URL
DB_ENGINE_URL_DWH = "postgresql+psycopg://pa_jas:P*ssw0rd_PA@103.59.160.166:5432/dwh"

DB_ENGINE_URL_CROCS = "postgresql+psycopg://pa_jas:P*ssw0rd_PA@103.59.160.166:5432/crocs"



# Create SQLAlchemy engine
dwh_engine = create_engine(
    DB_ENGINE_URL_DWH,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for SQL query logging
)

# Crocs SQLAlchemy engine (used by crocs routers)
crocs_engine = create_engine(
    DB_ENGINE_URL_CROCS,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,  # Set to True for SQL query logging
)
