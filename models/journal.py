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

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (title, content, timestamp, destination_id)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (self.title, self.content, self.timestamp, self.destination_id ))
        conn.commit()
        self.id = cursor.lastrowid

        return self


    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title DATE NOT NULL,
                content DATE NOT NULL,
                timestamp INTEGER NOT NULL,
                destination_id INTEGER NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Journal_entries table created")

Journal.create_table()
