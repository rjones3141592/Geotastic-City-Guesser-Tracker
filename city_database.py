import sqlite3
import os
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
        correct_city text NOT NULL,
        correct_state_country text NOT NULL,
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

def db_exists():
    return os.path.isfile('GT_stat_file.db')

# Checking if city_stats db file has any inputted values or if it is just blank.
def db_is_empty():
    if not db_exists():
        return True
    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT name FROM sqlite_master WHERE name = "city_stats"')
        if cursor.fetchone() is None:
            return True
        
        cursor.execute('SELECT COUNT(*) FROM city_stats')

        return cursor.fetchone()[0] == 0
    except sqlite3.OperationalError as error_code:
        print("Failed to add city. Error code: ", error_code)
        return True
    finally: 
        connection.close()

# Function to add city
def db_add(city_guess, stc_guess, was_correct, correct_city, correct_stc, guess_time = None):

    if city_guess == None:
        city_guess = 'Unknown City'
    
    if stc_guess == None:
        stc_guess = 'Unknown'
    
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

        most_recent_id = cursor.execute("SELECT id FROM city_stats ORDER BY id DESC LIMIT 1").fetchone()
        print((most_recent_id[0],))
        cursor.execute("DELETE FROM city_stats WHERE id = ?", (most_recent_id[0],))
        connection.commit()
    except sqlite3.OperationalError as error_code:
        print("Failed to remove most recent data!", error_code)
    finally: 
        connection.close()

# Function to read all data from the table to print onto table in guess history
def db_read_all():
    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        read_all = cursor.execute('SELECT id, guessed_city, guessed_state_country, correct_guess, correct_city, correct_state_country, guess_time, timestamp FROM city_stats ORDER BY id DESC')
        data = read_all.fetchall()
        return data
    
    except sqlite3.OperationalError as error_code:
        print('Failed to read data!', error_code)
        return None

    finally:
        connection.close()

def get_display_data():
    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        read_all = cursor.execute('SELECT id, guessed_city, guessed_state_country, correct_guess, correct_city, correct_state_country, guess_time, timestamp FROM city_stats ORDER BY id DESC')
        data = read_all.fetchall()

        display_data = []
        for row in data:
            row_list = list(row)

            if row_list[3] == 1:
                row_list[3] = 'Yes'
            else:
                row_list[3] = 'No'
            row = tuple(row_list)

            display_data.append(row)
        return display_data
    
    except sqlite3.OperationalError as error_code:
        print('Failed to read data!', error_code)
        return None

    finally:
        connection.close()


def db_delete_selected(id):
    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:

        delete_selected = cursor.execute("SELECT id FROM city_stats WHERE id = ?", (id,)).fetchone()
        cursor.execute("DELETE FROM city_stats WHERE id = ?", (delete_selected[0],))
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
