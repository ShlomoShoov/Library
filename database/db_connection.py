"""
This file is handle the Data Base connection and Tables setup and parameters

"""
import mysql.connector

HOST = '127.0.0.1'
PORT = 3315
USER = 'root'
PASSWORD = 'secret'
DATABASE = 'library_db'

def get_connection()->mysql.connector:
    """
    create connection to the database and return the connection 
    """
    config = {'host': HOST,
                  'user': USER,
                  'database': DATABASE,
                  'password': PASSWORD,
                  'port': PORT}
    
    return mysql.connector.connect(**config)


