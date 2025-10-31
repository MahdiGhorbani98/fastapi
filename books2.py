from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class BOOK:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, titel, author, description, rating):
        self.id = id
        self.titel = titel
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
    BOOK(1, 'B1', 'Ali', 'A nice book!', 5),
    BOOK(2, 'B2', 'Ehsan', 'A very nice book!', 4),
    BOOK(3, 'B3', 'Ali', 'A normal book!', 3)
]


@app.get('/books')
async def read_all_books():
    return BOOKS


@app.post('/create_book')
async def create_book(new_book: BookRequest):
    BOOKS.append(new_book)
