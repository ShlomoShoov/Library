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
                        email VARCHAR(255) UNIQUE NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        total_borrows INT DEFAULT 0
                        """
        self.create_table(cursor=cursor)

    x = 5
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
        return cursor.fetchone() is not None

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
    
    def get_member(self, cursor, member_id:int, lock:bool=False):
        query = f"""
                SELECT * FROM {self.table_name} 
                WHERE id=%s  {"FOR UPDATE" if lock else ""}
                """
        cursor.execute(query, (member_id,))
        return cursor.fetchone()
    
    def update_member(self, cursor, member_id, new_data):
        keys = [f"{key}=%s" for key in new_data.keys()]
        keys = ",".join(keys)
        values = list(new_data.values()) + [member_id]
        query = f"""
                UPDATE {self.table_name} SET 
                {keys} WHERE id=%s

     
                """
        cursor.execute(query, values)
        return cursor.rowcount > 0
    
    def increment_borrows(self, cursor, member_id):
        query = f"""
                UPDATE {self.table_name} SET total_borrows=total_borrows+1 WHERE id=%s
                """
        cursor.execute(query, (member_id,))

    def count_active_members(self, cursor)->int:
        key = 'cnt'
        query = f"""
                SELECT COUNT(*) AS {key} FROM {self.table_name} WHERE is_active=True
                """
        cursor.execute(query)
        res = cursor.fetchone()
        return res[key]

    def get_top_member(self, cursor)->dict:
        query = f"""
                SELECT * FROM {self.table_name} ORDER BY total_borrows DESC
                """
        cursor.execute(query)
        data = cursor.fetchone()
        return data



