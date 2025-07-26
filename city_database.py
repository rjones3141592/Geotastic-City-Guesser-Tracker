import sqlite3
connection = None

def db_startup():
    global connection
    # Creating file
    db_file = "GT_stat_file.db"

    # SQL Statement on table creation
    geotastic_stat_table = """CREATE TABLE IF NOT EXISTS city_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guessed_city text NOT NULL,
        guessed_state_country text NOT NULL,
        correct_guess BOOLEAN NOT NULL,
        correct_city text,
        correct_state_country text,
        guess_time FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    );"""

    # Try except to catch any issues with starting SQL connection
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Another try except, this time for table creation
        try:
            cursor.execute(geotastic_stat_table)
            connection.commit()
            
            print("Table created successfully!")
        except sqlite3.OperationalError as error_code:
            print("Failed to create database table! Eorr code: ", error_code)

    except sqlite3.OperationalError as error_code:
        print("Failed to open Stat Database! Error Code: ", error_code)
    finally:
        connection.close()

# Function to add city
def db_add(city_guess, stc_guess, was_correct, correct_city = None, correct_stc = None, guess_time = None):

    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO city_stats (guessed_city, guessed_state_country, correct_guess, correct_city, correct_state_country, guess_time) VALUES (?, ?, ?, ?, ?, ?)",(city_guess, stc_guess, was_correct, correct_city, correct_stc, guess_time))
        connection.commit()
    except sqlite3.OperationalError as error_code:
        print("Failed to add city. Error code: ", error_code)
    finally: 
        connection.close()

# Function to remove most recent city
def db_remove_recent():
    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:

        most_recent_id = cursor.execute("SELECT id FROM city_stats ORDER BY timestamp DESC LIMIT 1").fetchone()
        cursor.execute("DELETE FROM city_stats WHERE id = ?", (most_recent_id[0]))
        connection.commit()
    except sqlite3.OperationalError as error_code:
        print("Failed to remove most recent data!", error_code)
    finally: 
        connection.close()



def db_close():
    global connection
    if connection:
        connection.close()
        print("Successfully closed database!")
