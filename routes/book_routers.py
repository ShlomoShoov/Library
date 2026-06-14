"""
this file contain all of the routers that start with `book` 

"""

from fastapi import APIRouter, HTTPException
from database.book_db import NewBookModel, UpdateBookModel
from database.library_manager import LibraryManager
import database.library_manager as library_manager


router = APIRouter(prefix='/books')

manager = LibraryManager()

@router.post('',status_code=201)
def create_book(data:NewBookModel):
    manager.create_book(data.model_dump())

@router.get('')
def get_books():
    return manager.get_all_books()

@router.get("/{id}")
def get_book_by_id(id:int):
    try:
        return manager.get_book_by_id(book_id=id)
    except library_manager.BookNotExists:
        raise HTTPException(status_code=404, detail=f'{id} -> no such id or book, try use `/books` to find all ids')
    