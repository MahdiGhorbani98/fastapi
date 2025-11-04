from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    # Use Optional for id since it will be generated and not provided by the user
    id: Optional[int] = None
    # With Field, we can add validation constraints
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(1, 'B1', 'Ali', 'A nice book!', 5),
    Book(2, 'B2', 'Ehsan', 'A very nice book!', 4),
    Book(3, 'B3', 'Ali', 'A normal book!', 3)
]


@app.get('/books')
async def read_all_books():
    return BOOKS


@app.post('/create_book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(book_id_generator(new_book))


def book_id_generator(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
