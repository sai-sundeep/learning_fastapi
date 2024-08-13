"""
Author: Sai Sundeep Rayidi
Date: 8/1/2024

Description:
[Description of what the file does, its purpose, etc.]

Additional Notes:
[Any additional notes or information you want to include.]

License: 
MIT License

Copyright (c) 2024 Sai Sundeep Rayidi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contact:
[Optional: How to reach you for questions or collaboration.]

"""

from fastapi import FastAPI, Body
from fastapi import Path, Query, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from starlette import status

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


class BookCreateRequest(BaseModel):
    id: Optional[int] = Field(description="ID not required wile creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(gt=1990, lt=2025)

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "title": "Round Atlas",
    #                 "author": "Kevin Plum",
    #                 "description": "Excellent Novel",
    #                 "rating": 5,
    #                 "published_date": 2023
    #             }
    #         ]
    #     }
    # }

    model_config = ConfigDict(
        json_schema_extra= {
            "examples" : [
                {
                    "title": "Round Atlas",
                    "author": "Kevin Plum",
                    "description": "Excellent Novel",
                    "rating": 5,
                    "published_date": 2023
                }
            ]
        }
    )


BOOKS = [
    Book(1, "The Radiant Dawn", "Evelyn Harcourt", "Good book", 3, 2023),
    Book(2, "The Reversal", "Morgan Bellamy", "Good book", 3, 2022),
    Book(3, "The Infinite Horizon", "Jasper Kingsley", "Good book", 4, 2019),
    Book(4, "The Nexus", "Isla Connors", "Great Book", 4, 2020),
    Book(5, "Enchanted Realms", "Lena West", "Great book", 4, 2021),
    Book(6, "The Silent Haven", "Derek Lawson", "Excellent book", 5, 2022)
]


@app.get("/", status_code=status.HTTP_200_OK)
async def get_books():
    return "Welcome to Books API Application!"

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found!")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(ge=1, le=5)):
    result_books = []
    for book in BOOKS:
        if book.rating == book_rating:
            result_books.append(book)
    return result_books


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=1990, lt=2025)):
    result_books = []
    for book in BOOKS:
        if book.published_date == published_date:
            result_books.append(book)
    return result_books


def calc_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def add_a_book(incoming_book: BookCreateRequest):
    new_book = Book(**incoming_book.model_dump())
    BOOKS.append(calc_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book_by_id(book: BookCreateRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found!")


@app.delete("/books/{book_id_to_delete}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id_to_delete: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id_to_delete:
            BOOKS.pop(i)
            book_deleted = True
            break

    if not book_deleted:
        raise HTTPException(status_code=404, detail="Item not found!")