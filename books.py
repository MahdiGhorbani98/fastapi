from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"id": 1, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"id": 2, "title": "To Kill a Mockingbird",
        "author": "Harper Lee", "category": "Fiction"},
    {"id": 3, "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 4, "title": "The Lion",
        "author": "F. Scott Fitzgerald", "category": "Classic"}
]


@app.get('/books')
async def read_books():
    return BOOKS


@app.get('/books/my_books')
async def read_my_books():
    return {'message': 'List of my books'}


@app.get('/books/byauthor/{author}')
async def read_books_by_author(author: str):
    filtered_book = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            filtered_book.append(book)

    return filtered_book


@app.get('/books/{book_title}')
async def read_book(book_title: str):
    # Get with dynamic path "book_title"
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get('/books/')
async def read_books(category: str):
    # Get by query params "category"
    filtered_books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            filtered_books.append(book)
    return filtered_books


@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return "OK"


@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return "OK"


@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
