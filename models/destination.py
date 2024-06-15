import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()


class Destination:
    TABLE_NAME = "destination"
    DB_FILE = "db.sqlite"

    def __init__(self, name, image, location, description):
        self.id = None
        self.name = name
        self.image = image
        self.location = location
        self.description = description

    # saves to the database by excecuting INSERT query: adds the commited changes to the new inserted row
    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, image, location, description)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.image, self.location, self.description))
        conn.commit()
        self.id = cursor.lastrowid
        return self
    
    # updates to the database
    def update(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET name = ?, image = ?, location = ?, description = ?
        """
        cursor.execute(sql, (self.name, self.image, self.location, self.description, self.id))
        conn.commit()
        return self
    
    #returns a dictionary rep. of the table
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "description": self.description,
            "location": self.location
        }
    
    #retrieves all destinations from the database and returns they as a list
    @classmethod
    def find_all(cls):
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        destinations = []
        for row in rows:
            destination = cls(*row[1:])
            destination.id = row[0]
            destinations.append(destination)
        return destinations
    

    # retrieves destination by the given id
    @classmethod
    def find_by_id(cls, id):
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id =?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            destination = cls(*row[1:])
            destination.id = row[0]
            return destination
        return None
    
    @classmethod
    def create_table(cls):

        sql = f""" 
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image VARCHAR NOT NULL,
            location TEXT NOT NULL,
            description VARCHAR NOT NULL
            )
        """
        try:
            cursor.execute(sql)
            conn.commit()
            print("Destination table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

Destination.create_table()



