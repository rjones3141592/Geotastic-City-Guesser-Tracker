import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3

connection = None
# Default settings sql injection
default_settings = """INSERT OR IGNORE INTO settings (setting, value) VALUES ('dark_mode', False), ('confirm_exit', True), ('confirm_delete', True), ('confirm_reset', True), ('api_key', ''), ('rolling_number', 10)"""

def build_settings_frame(mainframe):
    header_label = ttk.Label(mainframe, text = "Settings:", font = ('Poppins',16))
    header_label.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    style = ttk.Style()
    style.configure("Custom.TCheckbutton", font = ('Poppins',12))

    dark_mode_button = ttk.Checkbutton(mainframe, text = "Dark Mode", style = "Custom.TCheckbutton")

    dark_mode_button.grid(row = 1, column = 0, sticky = 'w', pady = 5, padx = 5)

    dark_mode_var = tk.BooleanVar(value = read_setting('dark_mode'))

    dark_mode_button = ttk.Checkbutton(mainframe, variable = dark_mode_var, onvalue = True, offvalue = False, text = "Dark Mode", style = "Custom.TCheckbutton")

    dark_mode_button.grid(row = 1, column = 0, sticky = 'w', pady = 5, padx = 5)

    

def modify_darkmode():
    connection = sqlite3.connect('GT_settings.db')
    cursor = connection.cursor()

    dark_mode = cursor.execute("SELECT value FROM settings WHERE setting = 'dark_mode'")

    result = cursor.fetchone()
    
    swap_value = result[0]
    # Swapping value
    if (swap_value == True):
        swap_value = False
    else:
        swap_value = True

    cursor.execute("""UPDATE settings
                       SET value = ?
                       WHERE setting = 'dark_mode'""", (swap_value))
    
    connection.commit()
    connection.close()

def settings_startup():
    global connection
    # Creating file
    db_file = "GT_settings.db"

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
                return connection

            except sqlite3.OperationalError as error_code:
                print("Failed to establish default settings on startup! ", error_code)
            
            print("Settings successfully created!")
        except sqlite3.OperationalError as error_code:
            print("Failed to create settings! Error code: ", error_code)

    except sqlite3.OperationalError as error_code:
        print("Failed to open settings! Error Code: ", error_code)
    finally:
        
        connection.close() 

def read_setting(setting):
    connection = sqlite3.connect("GT_settings.db")
    cursor = connection.cursor()

    try:
        read_setting = cursor.execute('SELECT value FROM settings WHERE setting = ?', (setting,))
        value = read_setting.fetchone()

        if value[0] == 0 or value[0] == 1:
            return bool(int(value[0]))
        else:
            return value[0]
    
    except sqlite3.OperationalError as error_code:
            print("Failed to read settings!", error_code)

    finally:
        connection.close()

def settings_close():
    global connection
    if connection:
        connection.close()
        print("Successfully closed settings!")

        connection = None