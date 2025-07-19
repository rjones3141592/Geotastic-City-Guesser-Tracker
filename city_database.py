import sqlite3
connection = None

def db_startup():
    global connection
    # Creating file
    db_file = "GTStatFile.db"

    # SQL Statement on table creation
    geotastic_Stat_Table = """CREATE TABLE IF NOT EXISTS cityStats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guessed_city text NOT NULL,
        correct_guess BOOLEAN NOT NULL,
        correct_city text,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    );"""

    # Try except to catch any issues with starting SQL connection
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Another try except, this time for table creation
        try:
            cursor.execute(geotastic_Stat_Table)
            connection.commit()
            
            print("Table created successfully!")
        except sqlite3.OperationalError as error_code:
            print("Failed to create database table! Eorr code: ", error_code)

    except sqlite3.OperationalError as error_code:
        print("Failed to open Stat Database! Error Code: ", error_code)

def db_add(city_guess, was_correct, correct_city=None):
    pass

def db_close():
    global connection
    if connection:
        connection.close()
        print("Successfully closed database!")
