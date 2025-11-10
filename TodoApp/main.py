# Import FastAPI to create the web application
from fastapi import FastAPI

# Import models so SQLAlchemy knows about the table definitions
import models

# Import the database engine to connect and create tables
from database import engine

# Create the FastAPI app instance
app = FastAPI()

# Create database tables defined on models.Base if they don't already exist
models.Base.metadata.create_all(bind=engine)
