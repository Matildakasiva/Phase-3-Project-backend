import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

class Journal:
    TABLE_NAME = "journal_entries"

    def __init__(self, title, content, timestamp, destination_id):
        self.id = None
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.destination_id = destination_id

    # saves to the database by excecuting INSERT query: adds the commited changes to the new inserted row 
    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (title, content, timestamp, destination_id)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (self.title, self.content, self.timestamp, self.destination_id ))
        conn.commit()
        self.id = cursor.lastrowid
        return self
    
    #returns a dictionary rep. of the table
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
            "destination_id": self.destination_id
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
            return journal
        return None
    
    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATE NOT NULL,
                destination_id INTEGER NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Journal_entries table created")

Journal.create_table()
