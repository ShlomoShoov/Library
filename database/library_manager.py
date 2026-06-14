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
from database.db_connection import Connection
from database.book_db import BookTableManager
from database.member_db import MemberTableManagement

connection = Connection()
get_connection = connection.get_connection

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


class BookIsBorrowed(Exception):
    """
    raise  when we try to return a book for a user that borrowed to other user
    """
    pass


class UserInactive(Exception):
    """
    when we try to borrow book from inactive user
    """
    pass


class OverTheBarrowLimit(Exception):
    """
    we try to barrow a book for a user but it has 3 books borrowed

    """
    pass


class BookIsBorrowedToOtherUser(Exception):
    """
    when we try to return a book for a user that borrowed to other user
    """
    pass


class LibraryManager:
    def __init__(self):
        self.book_manager = self.get_table_manager(BookTableManager)
        self.member_manager = self.get_table_manager(MemberTableManagement)
        self.max_books = 3

    def get_table_manager(self, table_class) -> BookTableManager | MemberTableManagement:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                return table_class(cursor=cursor)

    def create_book(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                self.book_manager.create_book(cursor=cursor, data=data)
                conn.commit()

    def create_member(self, data: dict):
        with get_connection() as conn:
            with conn.cursor(buffered=True) as cursor:
                email = data['email']
                if self.member_manager.is_email_exists(cursor=cursor, email=email):
                    raise EmailExist

                self.member_manager.create_member(cursor=cursor, data=data)
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

    def get_book_by_id(self, book_id: int, lock: bool = False):
        with get_connection() as conn:
            with conn.cursor(dictionary=True, buffered=True) as cursor:
                book = self.book_manager.get_book(
                    cursor=cursor, book_id=book_id, lock=lock)

        if book is None:
            raise BookNotExists
        return book

    def get_member_by_id(self, member_id: int, lock: bool = False):
        with get_connection() as conn:
            with conn.cursor(dictionary=True, buffered=True) as cursor:
                member = self.member_manager.get_member(
                    cursor=cursor, member_id=member_id, lock=lock)

        if member is None:
            raise UserNotExists
        return member

    def update_book(self, book_id: int, new_data: dict):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if not new_data:
                    return

                has_update = self.book_manager.update_book(cursor=cursor,
                                                           book_id=book_id,
                                                           new_data=new_data)

                if not has_update:
                    conn.rollback()
                    raise BookNotExists

                else:
                    conn.commit()

    def update_member(self, member_id: int, new_data: dict):
        with get_connection() as conn:
            with conn.cursor(buffered=True) as cursor:
                if not new_data:
                    return

                email = new_data.get('email')
                if email is not None:
                    if self.member_manager.is_email_exists(cursor=cursor, email=email):
                        conn.rollback()
                        raise EmailExist

                has_update = self.member_manager.update_member(cursor=cursor,
                                                               member_id=member_id,
                                                               new_data=new_data)

                if not has_update:
                    conn.rollback()
                    raise UserNotExists
                else:
                    conn.commit()

    def borrow_book(self, book_id: int, member_id: int):
        with get_connection() as conn:
            with conn.cursor(buffered=True, dictionary=True) as cursor:
                book_data = self.book_manager.get_book(
                    cursor=cursor, book_id=book_id, lock=True)
                user_data = self.member_manager.get_member(
                    cursor=cursor, member_id=member_id, lock=True)
                if book_data is None:
                    raise BookNotExists
                if user_data is None:
                    raise UserNotExists
                if not book_data['is_available']:
                    conn.rollback()
                    raise BookIsBorrowed
                if not user_data['is_active']:
                    conn.rollback()
                    raise UserInactive

                member_borrowed_books = self.book_manager.count_active_borrows_by_member(
                    cursor=cursor, member_id=member_id)

                if member_borrowed_books > self.max_books:
                    conn.rollback()
                    raise OverTheBarrowLimit(
                        f'max books to barrow -> {self.max_books} | books borrow now -> {member_borrowed_books}')

                update_data_book = {"is_available": False,
                                    "borrowed_by_member_id": member_id}
                self.book_manager.update_book(
                    cursor=cursor, book_id=book_id, new_data=update_data_book)
                self.member_manager.increment_borrows(
                    cursor=cursor, member_id=member_id)
                conn.commit()

    def return_book(self, book_id: int, member_id: int):
        with get_connection() as conn:
            with conn.cursor(buffered=True, dictionary=True) as cursor:
                book_data = self.book_manager.get_book(
                    cursor=cursor, book_id=book_id, lock=True)
                user_data = self.member_manager.get_member(
                    cursor=cursor, member_id=member_id, lock=True)
                if book_data is None:
                    raise BookNotExists
                if user_data is None:
                    raise UserNotExists
                if book_data['borrowed_by_member_id'] != member_id:
                    conn.rollback()
                    raise BookIsBorrowedToOtherUser

                update_data_book = {"is_available": True,
                                    "borrowed_by_member_id": None}
                self.book_manager.update_book(
                    cursor=cursor, book_id=book_id, new_data=update_data_book)
                conn.commit()

    def activate_member(self, member_id):
        update_data = {"is_active": True}
        self.update_member(member_id=member_id, new_data=update_data)

    def deactivate_member(self, member_id):
        update_data = {"is_active": False}
        self.update_member(member_id=member_id, new_data=update_data)

    def get_summary(self):
        with get_connection() as conn:
            with conn.cursor(buffered=True, dictionary=True) as cursor:
                all_books_cnt = self.book_manager.cnt_all_books(cursor=cursor)
                available_books = self.book_manager.cnt_available_books(cursor=cursor)
                unavailable_books = all_books_cnt- available_books
                active_members = self.member_manager.count_active_members(cursor=cursor)
                return {
                    "total_books": all_books_cnt,
                    "available_books": available_books,
                    "currently_borrowed": unavailable_books,
                    "active_members": active_members
                    }
            
    def get_books_by_genre(self):
        with get_connection() as conn:
            with conn.cursor(buffered=True, dictionary=True) as cursor:
                return self.book_manager.get_cnt_by_genre(cursor)
            
    def get_top_member(self):
        with get_connection() as conn:
            with conn.cursor(buffered=True, dictionary=True) as cursor:
                return self.member_manager.get_top_member(cursor)
            