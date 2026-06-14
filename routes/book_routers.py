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
    manager.create_book(data.model_dump(exclude_none=True))

@router.get('')
def get_books():
    return manager.get_all_books()

@router.get("/{id}")
def get_book_by_id(id:int):
    try:
        return manager.get_book_by_id(book_id=id)
    except library_manager.BookNotExists:
        raise HTTPException(status_code=404, detail=f'{id} -> no such id or book, try use `/books` to find all ids')
    
@router.put("/{id}")
def update_book(id:int,new_data:UpdateBookModel):
    try:
        manager.update_book(book_id=id, new_data=new_data.model_dump(exclude_none=True))

    except library_manager.BookNotExists:
        raise HTTPException(status_code=404, detail=f'you can not update {id} -> is not exists')
    

@router.put("/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id:int):
    try:
        manager.borrow_book(book_id=id,member_id=member_id)

    except library_manager.BookNotExists:
        raise HTTPException(status_code=404, detail=f'you can not borrow {id} -> is not exists')
    
    except library_manager.UserNotExists:
        raise HTTPException(
            status_code=404, detail=f"{id} -> member not found")
    
    except library_manager.BookIsBorrowed:
        raise HTTPException(status_code=400, detail=f"book {id} is borrowed ")
    
    except library_manager.UserInactive:
        raise HTTPException(status_code=400, detail=f"user {id} is inactive")
    
    except library_manager.OverTheBarrowLimit as e:
        error_details = e.args[0]
        raise HTTPException(status_code=400, detail=f"you reach the limit of book borrowing: {error_details} ")

# @router.put("/{id}/return/{member_id}")
# def return_book()