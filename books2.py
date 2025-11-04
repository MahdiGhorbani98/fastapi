from fastapi import Body, FastAPI
from pydantic import BaseModel

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
    id: int
    title: str
    author: str
    description: str
    rating: int


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
    BOOKS.append(new_book)
