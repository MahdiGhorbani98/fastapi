from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    # Use Optional for id since it will be generated and not provided by the user
    id: Optional[int] = Field(
        description="The ID will be generated automatically", default=None)
    # With Field, we can add validation constraints
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1800)

    # Adding example data for better documentation
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book Model",
                "author": "Darling",
                "description": "A model representing a book",
                "rating": 5,
                "published_date": 2010
            }
        }
    }


BOOKS = [
    Book(1, 'B1', 'Ali', 'A nice book!', 5, 2015),
    Book(2, 'B2', 'Ehsan', 'A very nice book!', 4, 2018),
    Book(3, 'B3', 'Ali', 'A normal book!', 3, 2019)
]


@app.get('/books')
async def read_all_books():
    return BOOKS


@app.get('/books/static')
async def read_book():
    print('static path')


@app.get('/books/{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get('/books/')
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    filtered_books = []
    for book in BOOKS:
        if book.rating == rating:
            filtered_books.append(book)
    return filtered_books


@app.get('/books/publish/')
async def read_book_by_date(date: int = Query(gt=1800)):
    filtered_books = []
    for book in BOOKS:
        if book.published_date == date:
            filtered_books.append(book)
    return filtered_books


@app.post('/create_book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(book_id_generator(new_book))


def book_id_generator(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put('/books/update_book')
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete('/books/{book_id}')
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
