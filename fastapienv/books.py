# Created by Sai at 6/26/2024

from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "author one", "name": "Introduction to Programming", "category": "Computer Science"},
{"title": "Title Two", "author": "author two", "name": "Introduction to Maths", "category": "Maths"},
{"title": "Title Three", "author": "author three", "name": "Introduction to Physics", "category": "Physics"},
{"title": "Title Four", "author": "author four", "name": "Introduction to Geography", "category": "Geography"},
{"title": "Title Five", "author": "author five", "name": "Introduction to Computer Science", "category": "Computer Science"},
{"title": "Title Six", "author": "author six", "name": "Introduction to History", "category": "History"},
{"title": "Title Seven", "author": "author seven", "name": "Introduction to Economics", "category": "Economics"},
{"title": "Title Eight", "author": "author eight", "name": "Introduction to Economics", "category": "Economics"},
{"title": "Title Twenty Two", "author": "author two", "name": "Introduction to Linear Algebra", "category": "Maths"},
]


# Simple Get Method Demo
@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "my_favoutite_book"}


# Path Parameters Demo
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# Query Parameters Demo
@app.get("/books/")
async def get_books_by_category(category: str):
    result_books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            result_books.append(book)
    return result_books


# Path and Query Parameters Together
@app.get("/books/author_name/")
async def get_books_by_author_category(author_name: str, category: str):
    result_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold() and book.get("category").casefold() == category.casefold():
            result_books.append(book)
    return result_books


# Post Request Demo
@app.post("/books/create_book")
async def add_a_book(newbook=Body()):
    BOOKS.append(newbook)


# Put Request Demo
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


# Delete Request Demo
@app.delete("/books/delete_book/{book_title}")
async def delete_a_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# API Endpoint to fetch all books by an author - Path Parameter Solution
@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str):
    result_books = []

    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            result_books.append(book)

    return result_books


# API Endpoint to fetch all books by an author - Path Parameter Solution
@app.get("/books/author/")
async def get_books_by_author(author_name: str):
    result_books = []

    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            result_books.append(book)

    return result_books