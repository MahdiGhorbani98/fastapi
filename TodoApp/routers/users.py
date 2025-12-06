# Import FastAPI to create the web application
from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

# Import models so SQLAlchemy knows about the table definitions
from models import Users
# Import the database engine to connect and create tables
from database import SessionLocal

# Create the FastAPI app instance
router = APIRouter(prefix='/user',
                   tags=['user'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(
        user_verification.new_password)
    db.add(user_model)
    db.commit()
