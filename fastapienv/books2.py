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
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Books:
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


class BookCreateRequest(BaseModel):
    id: Optional[int] = Field(description="ID not required wile creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Round Atlas",
                    "author": "Kevin Plum",
                    "description": "Excellent Novel",
                    "rating": 5
                }
            ]
        }
    }


BOOKS = [
    {"id": 1, "title": "The Radiant Dawn", "author": "Evelyn Harcourt", "description": "Good book", "rating": 3},
    {"id": 2, "title": "The Reversal", "author": "Morgan Bellamy", "description": "Good book", "rating": 3},
    {"id": 3, "title": "The Infinite Horizon", "author": "Jasper Kingsley", "description": "Good book", "rating": 4},
    {"id": 4, "title": "The Nexus", "author": "Isla Connors", "description": "Great Book", "rating": 4},
    {"id": 5, "title": "Enchanted Realms", "author": "Lena West", "description": "Great book", "rating": 4},
    {"id": 6, "title": "The Silent Haven", "author": "Derek Lawson", "description": "Excellent book", "rating": 5}
]


def calc_book_id(book: Books):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1]["id"] + 1
    return book


@app.get("/books")
async def get_books():
    return BOOKS


@app.post("/create_book")
async def add_a_book(incoming_book: BookCreateRequest):
    new_book = Books(**incoming_book.model_dump())
    BOOKS.append(calc_book_id(new_book))