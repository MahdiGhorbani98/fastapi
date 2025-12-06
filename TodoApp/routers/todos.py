# Import FastAPI to create the web application
from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user

# Import models so SQLAlchemy knows about the table definitions
from models import Todos
# Import the database engine to connect and create tables
from database import SessionLocal

# Create the FastAPI app instance
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# This line defines a dependency used in FastAPI route functions to get information about the current user.
#
# - 'Depends' is a FastAPI feature to declare something as a dependency. When a route function uses a parameter with Depends(some_function),
#   FastAPI will automatically call 'some_function' and use its return value as the parameter value.
# - 'get_current_user' is a function (usually defined in your authentication code) that retrieves and verifies the user from the request, such as by reading a token.
# - 'Annotated[dict, Depends(get_current_user)]' is a way to specify both the type (here, a dictionary) and additional metadata (the dependency).
#   In this case, it says: "This is a dict, but to get its value, FastAPI should call get_current_user via Depends."
#
# So, 'user_dependency' can be used as a parameter type in routes, and FastAPI will handle user authentication transparently.
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Task title",
                "description": "Task description",
                "priority": 5,
                "complete": False
            }
        }
    }


@router.get('/', status_code=status.HTTP_200_OK)
# ? When we add user: user_dependency for funtions as params, the endpoint convert to a private endpoint
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    # db.delete(todo_model)
    db.commit()
