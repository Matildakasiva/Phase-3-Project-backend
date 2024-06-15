import sqlite3


conn = sqlite3.connect("db.sqlite")
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
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, image, attractions, festivals, accomodation, vehicle_rentals)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.image, self.attractions, self.festivals, self.accomodation, self.vehicle_rentals))
        conn.commit()
        self.id = cursor.lastrowid
        return self
    
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
            "festivals": self.festivals,
            "attractions": self.attractions
        }
    
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
        finally:
            conn.close()

Details.create_table()