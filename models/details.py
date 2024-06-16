import sqlite3
import json

conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

class Details:
    TABLE_NAME = "details"
    DB_FILE = "db.sqlite"

    def __init__(self, name, image, attractions, festivals, accomodation, vehicle_rentals):
        self.id = None
        self.name = name
        self.image = image
        self.attractions = attractions
        self.festivals = festivals
        self.accomodation = accomodation
        self.vehicle_rentals = vehicle_rentals

    # saves to the database by excecuting INSERT query: adds the commited changes to the new inserted row
    def save(self):
        #converts a list into a string
        self.attractions = json.dumps(self.attractions)
        self.accomodation = json.dumps(self.accomodation)
        self.vehicle_rentals = json.dumps(self.vehicle_rentals)

        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, image, attractions, festivals, accomodation, vehicle_rentals)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.image, self.attractions, self.festivals, self.accomodation, self.vehicle_rentals))
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
            SET name = ?, image = ?, attractions = ?, festivals = ? accomodation = ?, vehicle_rentals = ?
        """
        cursor.execute(sql, (self.name, self.image, self.attractions, self.festivals, self.accomodation, self.vehicle_rentals))
        conn.commit()
        return self
    
    #returns a dictionary rep. of the table
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "festivals": json.dumps(self.festivals),
            "attractions": json.dumps(self.attractions),
            "vehicle_rentals": json.dumps(self.vehicle_rentals)
        }
    
    # retrieves details from the database and returns a list of all the details
    @classmethod
    def find_all(cls):
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        details = []
        for row in rows:
            detail = cls(*row[1:])
            detail.id = row[0]

            #converts list to a string
            detail.attractions = json.loads(detail.attractions)
            detail.accomodation = json.loads(detail.accomodation)
            detail.vehicle_rentals = json.loads(detail.vehicle_rentals)

            details.append(detail)
        return details
    
    #retrieves details by the id given
    @classmethod
    def find_by_id(cls, id):
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id =?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            detail = cls(*row[1:])
            detail.id = row[0]
            return detail
        return None
    
    @classmethod
    def create_table(cls):

        sql = f""" 
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image VARCHAR NOT NULL,
            attractions TEXT NOT NULL,
            festivals VARCHAR NOT NULL,
            accomodation TEXT NOT NULL,
            vehicle_rentals TEXT NOT NULL
            )
        """
        try:
            cursor.execute(sql)
            conn.commit()
            print("Destination details table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
        

Details.create_table()