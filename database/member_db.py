""" 
this file is response to the table `members`

**classes**

`MemberTableManagement` -> response to all of the crud actions 
and define the table schema
`NewMemberModel` -> pydantic class that define how should you send 
a new member details
`UpdateMemberModel` -> pydantic class that define how would an update 
should looks like


"""
from pydantic import BaseModel
import mysql.connector.cursor


class NewMemberModel(BaseModel):
    name: str
    email : str

class UpdateMemberModel(BaseModel):
    name: str | None = None
    email : str | None = None

class MemberTableManagement:
    def __init__(self, cursor:mysql.connector.cursor):
        self.table_name = 'members'
        self.schema = """
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        total_borrows INT DEFAULT 0
                        """
        self.create_table(cursor=cursor)

    def create_table(self, cursor:mysql.connector.cursor):
        """
        create the function if not exists, due to the schema define
        in self.schema
        """
        query = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name}
                ({self.schema})
                """
        cursor.execute(query)

    def is_email_exists(self ,cursor, email:str)->bool:
        """
        this function check if email is already exists in 
        the table, return True or False
        
        """
        query = f"""
                SELECT * from {self.table_name} WHERE email=%s
                """
        cursor.execute(query, (email,))
        return cursor.rowcount == 0

    def create_member(self, cursor, data:dict):
        """
        execute insert query to add data
        """
        keys = ",".join(data.keys())
        values = list(data.values())
        values_template = ",".join(["%s"]*len(values))
        query = f"""
                INSERT INTO {self.table_name} ({keys}) 
                VALUES ({values_template})
                """
        cursor.execute(query, values)

    def get_all_members(self, cursor):
        query = f"""
                SELECT * FROM {self.table_name}
                """
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_member(self, cursor, member_id:int):
        query = f"""
                SELECT * FROM {self.table_name} 
                WHERE id=%s
                """
        cursor.execute(query, (member_id,))
        return cursor.fetchone()



