import sqlite3
import datetime

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

class Journaling:
    TABLE_NAME = "my_journal_entries"
    
    #args = used to a pass variable number of arguments
    def __init__(self, *args):
        if len(args) == 2:
            self.id = None
            self.title, self.content = args
            self.timestamp = datetime.datetime.now()
        elif len(args) == 3:
            self.id, self.title, self.content = args
            self.timestamp = datetime.datetime.now()
        elif len(args) == 4:
            self.id, self.title, self.content, self.timestamp = args
        else:
            raise ValueError("Invalid number of arguments")

    # saves to the database by excecuting INSERT query: adds the commited changes to the new inserted row 
    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (title, content)
            VALUES (?, ?)
        """
        cursor.execute(sql, (self.title, self.content))
        conn.commit()
        self.id = cursor.lastrowid
        return self
    
     #deletes from the database
    def delete(self):
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
    
    # updates to the database
    def update(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET title = ?, content = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.title, self.content, self.id))
        conn.commit()
        return self
    
    #returns a dictionary rep. of the table
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    #retrieves journal_entries from the database
    @classmethod
    def find_all(cls):
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        journals = []
        for row in rows:
            journal = cls(*row[1:])
            journal.id = row[0] 
            journal.timestamp = row[3]
            journals.append(journal)
        return journals
    
    #retrieves journal_entries of a given id
    @classmethod
    def find_by_id(cls, id):
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id =?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            journal = cls(*row[1:])
            journal.id = row[0]
            journal.timestamp = row[3]
            return journal
        return None
    
    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Journal_entries table created")

Journaling.create_table()

# cursor.execute(f"DROP TABLE IF EXISTS {Journal.TABLE_NAME}")
# conn.commit()
# print("Journal_entries table deleted")
# cursor.execute("ALTER TABLE my_journal_entries DROP COLUMN timestamp")
# conn.commit()
# print("timestamp column deleted")

