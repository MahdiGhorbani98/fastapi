# Import FastAPI to create the web application
from fastapi import FastAPI
from routers import auth, todos, admin, users

# Import models so SQLAlchemy knows about the table definitions
import models
# Import the database engine to connect and create tables
from database import engine

# Create the FastAPI app instance
app = FastAPI()

# Create database tables defined on models.Base if they don't already exist
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
