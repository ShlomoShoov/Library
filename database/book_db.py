"""
This file response on the Table `book`:

**Classes**

- `BookTableManager` class that handle CRUD methods 
with the `book` Table

- Pydantic Model Classes
`NewBookModel` and `UpdateBookModel` that config the Model to define what dict should 
the end user send to create or update a book.

"""

from pydantic import BaseModel
from typing import Literal
import mysql.connector.cursor


class NewBookModel(BaseModel):
    title: str
    author: str
    genre: Literal['Fiction', 'Non-Fiction',
                   'Science', 'History', 'Other'] | None = None


class UpdateBookModel(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Literal['Fiction', 'Non-Fiction',
                   'Science', 'History', 'Other'] | None = None


class BookTableManager:
    def __init__(self, cursor: mysql.connector.cursor):
        self.table_name = 'books'
        self.schema = """
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction','Science', 'History', 'Other'),
                        is_available BOOLEAN DEFAULT TRUE ,
                        borrowed_by_member_id INT
                        """
        self.create_table(cursor=cursor)

    def create_table(self, cursor: mysql.connector.cursor):
        query = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name}
                ({self.schema})
                """
        cursor.execute(query)

    def create_book(self, cursor: mysql.connector.cursor, data: dict):
        keys = ",".join(data.keys())
        values = list(data.values())
        values_template = ",".join(["%s"]*len(values))
        query = f"""
                INSERT INTO {self.table_name} ({keys}) 
                VALUES ({values_template})
                """
        cursor.execute(query, values)

    def get_all_books(self, cursor) -> list[dict]:
        query = f"""
                SELECT * FROM {self.table_name}
                """
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_book(self,cursor, book_id:int):
        query = f"""
                SELECT * FROM {self.table_name} 
                WHERE id=%s
                """
        cursor.execute(query, (book_id,))
        return cursor.fetchone()

