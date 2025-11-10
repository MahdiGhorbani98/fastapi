# Import the create_engine function to establish database connections
from sqlalchemy import create_engine

# Import sessionmaker to create database session objects for queries
from sqlalchemy.orm import sessionmaker

# Import declarative_base to create the base class for database models
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL - using SQLite with a local file called todos.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the database engine that manages connections to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
    'check_same_thread': False})  # Allow multiple threads to use the same connection

# Create a session factory that generates database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class that all your database models will inherit from
Base = declarative_base()

# ? Extra information
# I'll add comments to explain each line and then explain the key concepts.

# Simple Explanations:
# SQLAlchemy: A Python library that lets you interact with databases using Python code instead of writing SQL queries directly. It's like a translator between Python and databases.

# ORM (Object-Relational Mapping): A technique that maps your Python classes to database tables. Instead of working with raw SQL, you work with Python objects that automatically sync with the database.

# Key Components in Your Code:

# Engine → The connection manager to your database
# Session → A temporary connection used to query and save data
# Base → The parent class for creating database models (tables)
