"""
This file is handle the Data Base connection and Tables setup and parameters

"""
import mysql.connector

class Connection:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 3315
        self.USER = 'root'
        self.PASSWORD = 'secret'
        self.DATABASE = 'library_db'

    def get_connection(self)->mysql.connector:
        """
        create connection to the database and return the connection 
        """
        config = {'host': self.HOST,
                    'user': self.USER,
                    'database':self.DATABASE,
                    'password': self.PASSWORD,
                    'port': self.PORT}
        
        return mysql.connector.connect(**config)


