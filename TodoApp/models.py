# Import Base class from database.py to inherit table structure
from database import Base

from sqlalchemy import Column, Integer, String, Boolean

# Define the Todos model (represents a table in the database)


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    priority = Column(Integer)

    complete = Column(Boolean, default=False)
