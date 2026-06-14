"""
this file contain all of the routers that start with `book` 

"""

from fastapi import APIRouter, HTTPException
from database.book_db import NewBookModel, UpdateBookModel
from database.library_manager import LibraryManager

router = APIRouter(prefix='/books')

manager = LibraryManager()

@router.post('',status_code=201)
def create_book(data:NewBookModel):
    manager.create_book(data.model_dump())

@router.get('')
def get_books():
    return manager.get_all_books()