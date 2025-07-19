import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3

connection = None
# Default settings sql injection
default_settings = """INSERT OR IGNORE INTO settings (setting, value) VALUES ('darkMode', False), ('confirmExit', True), ('confirmDelete', True)"""

def build_settings_frame(mainframe):
    label1 = ttk.Label(mainframe, text = "Settings!", justify = 'left', font = ('Poppins',15))
    label1.configure()

    style = ttk.Style()
    style.configure("Custom.TCheckbutton", font = ('Poppins',15))

    darkMode_button = ttk.Checkbutton(mainframe, text = "Change appearance", style = "Custom.TCheckbutton")

    label1.pack(pady=10, padx = 5, anchor = 'w')
    darkMode_button.pack(pady = 5, padx = 5, anchor = 'w')


def modify_darkmode():
    connection = sqlite3.connect('GTSettings.db')
    cursor = connection.cursor()

    darkMode = cursor.execute("SELECT value FROM settings WHERE setting = 'darkMode'")

    result = cursor.fetchone()
    
    swap_value = result[0]
    # Swapping value
    if (swap_value == '1'):
        swap_value = '0'
    else:
        swap_value = '1'

    cursor.execute("""UPDATE settings
                       SET value = ?
                       WHERE setting = 'darkMode'""", (swap_value))
    
    connection.commit()
    connection.close()

        

def settings_startup():
    global connection
    # Creating file
    db_file = "GTSettings.db"

    # SQL Statement on settings
    settings_table = """CREATE TABLE IF NOT EXISTS settings (
        setting TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );"""

    # Try except to catch any issues with starting SQL connection
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Another try except, this time for table creation
        try:
            cursor.execute(settings_table)
            connection.commit()

            # One last try to create default settings
            try:
                cursor.execute(default_settings)
                connection.commit()
                print("Successfully set default settings!")

            except sqlite3.OperationalError as error_code:
                print("Failed to establish default settings on startup! ", error_code)
            
            print("Settings successfully created!")
        except sqlite3.OperationalError as error_code:
            print("Failed to create settings! Error code: ", error_code)

    except sqlite3.OperationalError as error_code:
        print("Failed to open settings! Error Code: ", error_code)
    
    return connection





def settings_close():
    global connection
    if connection:
        connection.close()
        print("Successfully closed settings!")

        connection = None