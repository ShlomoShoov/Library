"""
this file contain all of the routers that start with `book` 

"""

from fastapi import APIRouter, HTTPException
from database.book_db import NewBookModel, UpdateBookModel
from database.library_manager import LibraryManager
import database.library_manager as library_manager
from logs.logs_config import get_logger

logger = get_logger()

router = APIRouter(prefix='/books')

manager = LibraryManager()

@router.post('',status_code=201)
def create_book(data:NewBookModel):
    manager.create_book(data.model_dump(exclude_none=True))
    logger.info('added new book; %s'(data,))

@router.get('')
def get_books():
    return manager.get_all_books()

@router.get("/{id}")
def get_book_by_id(id:int):
    try:
        return manager.get_book_by_id(book_id=id)
    except library_manager.BookNotExists:
        logger.warning('trying to get book id -> %s but it is not exists',(id,))
        raise HTTPException(status_code=404, detail=f'{id} -> no such id or book, try use `/books` to find all ids')
    
@router.put("/{id}")
def update_book(id:int,new_data:UpdateBookModel):
    try:
        manager.update_book(book_id=id, new_data=new_data.model_dump(exclude_none=True))
        logger.info('book id - %s updated, new data: %s',(id,new_data))
    except library_manager.BookNotExists:
        logger.warning('trying to update book id -> %s but it is not exists',(id,))
        raise HTTPException(status_code=404, detail=f'you can not update {id} -> is not exists')
    

@router.put("/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id:int):
    try:
        manager.borrow_book(book_id=id,member_id=member_id)

    except library_manager.BookNotExists:
        logger.warning('trying to borrow book id -> %s but it is not exists',(id,))
        raise HTTPException(status_code=404, detail=f'you can not borrow {id} -> is not exists')
    
    except library_manager.UserNotExists:
        logger.warning('tried to borrow book for user id %s but user does not exist',(member_id,))
        raise HTTPException(
            status_code=404, detail=f"{id} -> member not found")
    
    
    except library_manager.BookIsBorrowed:
        logger.warning('tries to borrow book id %s - book is already borrowed',(id,))
        raise HTTPException(status_code=400, detail=f"book {id} is borrowed ")
    
    except library_manager.UserInactive:
        logger.warning('tries to borrow book for user id %s but user is inactive',(member_id,))
        raise HTTPException(status_code=400, detail=f"user {id} is inactive")
    
    except library_manager.OverTheBarrowLimit as e:
        error_details = e.args[0]
        logger.warning('tries to borrow book for user id %s but user is out of the  limit of books : %s'(member_id,error_details))
        raise HTTPException(status_code=400, detail=f"you reach the limit of book borrowing: {error_details} ")

@router.put("/{id}/return/{member_id}")
def return_book(id:int, member_id:int):
    try:
        manager.return_book(book_id=id, member_id=member_id)
    except library_manager.BookNotExists:
        logger.warning('tries to return book id %s but book does not exists', (id,))
        raise HTTPException(status_code=404, detail=f'you can not return book id- {id} -> is not exists')
    
    except library_manager.UserNotExists:
        logger.warning('tried to return book for user id %s but user does not exist',(member_id,))
        raise HTTPException(
            status_code=404, detail=f"{id} -> member not found")
    
    except library_manager.BookIsBorrowedToOtherUser:
        logger.warning('tries to return book id %s from user id %s but the book is not borrowed to this user', (id, member_id))
        raise HTTPException(
            status_code=400, detail=f"book {id} is not borrowed to {member_id}"
        )