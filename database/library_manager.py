"""
This file is response for all of the actions 
on the library.

**classes**
`LibraryManager` class that handle of the action
needed for the library management.

- Errors Classes
*errors connected to books*
`BookNotExists` -> when we try to found or do things about a book that does not exists.
`BookIsBorrowed` -> when we try to borrow a book is already borrowed.
`BookIsBorrowedToOtherUser` -> when we try to return a book for a user that borrowed to other user

*errors connected to users*
`UserNotExists` -> we try to find or do an action on a user that does not exists
`UserInactive` -> when we try to borrow book from inactive user
`MailExist` -> we try to create or update a mail with a mail that exists
`OverTheBarrowLimit` -> we try to barrow a book for a user but it has 3 books borrowed

"""
from database.db_connection import get_connection
from database.book_db import BookTableManager
from database.member_db import MemberTableManagement


class EmailExist(Exception):
    """
     we try to create or update a mail with a mail that exists

    """
    pass

class BookNotExists(Exception):
    """
    when we try to found or do things about a book that does not exists.
    """
    pass

class UserNotExists(Exception):
    """
    
    we try to find or do an action on a user that does not exists
    """
    pass


class LibraryManager:
    def __init__(self):
          self.book_manager = self.get_table_manager(BookTableManager)
          self.member_manager = self.get_table_manager(MemberTableManagement)
        
    def get_table_manager(self, table_class)->BookTableManager|MemberTableManagement:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                return table_class(cursor=cursor)
            
    def create_book(self, data:dict):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                self.book_manager.create_book(cursor=cursor, data=data)
                conn.commit()

    def create_member(self,data:dict):
        with get_connection() as conn:
            with conn.cursor(buffered=True) as cursor:
                email = data['email']
                if not self.member_manager.is_email_exists(cursor=cursor, email=email):
                    raise EmailExist

                self.member_manager.create_member(cursor=cursor,data=data)
                conn.commit()

    def get_all_books(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                books = self.book_manager.get_all_books(cursor=cursor)
                
        return books
    
    def get_all_members(self):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                members = self.member_manager.get_all_members(cursor=cursor)

        return members
    

    def get_book_by_id(self, book_id:int):
        with get_connection() as conn:
            with conn.cursor(dictionary=True,buffered=True) as cursor:
                book = self.book_manager.get_book(cursor=cursor, book_id=book_id)

        if book is None:
            raise BookNotExists
        return book
    
        
    def get_member_by_id(self, member_id:int):
        with get_connection() as conn:
            with conn.cursor(dictionary=True, buffered=True) as cursor:
                member = self.member_manager.get_member(cursor=cursor, member_id=member_id)

        if member is None:
            raise UserNotExists
        return member
        