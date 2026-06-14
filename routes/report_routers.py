import  database.library_manager as library_manager
from fastapi import APIRouter

router  = APIRouter(prefix="/reports")

manager = library_manager.LibraryManager()

@router.get("/summary")
def get_summary():
    return manager.get_summary()

@router.get("/books-by-genre")
def get_books_by_genre():
    return manager.get_books_by_genre()

@router.get("/top-member")
def get_top_member():
    return manager.get_top_member()

