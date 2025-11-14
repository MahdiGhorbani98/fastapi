# Import FastAPI to create the web application
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

# Import models so SQLAlchemy knows about the table definitions
import models
from models import Todos
# Import the database engine to connect and create tables
from database import SessionLocal, engine

# Create the FastAPI app instance
app = FastAPI()

# Create database tables defined on models.Base if they don't already exist
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")
