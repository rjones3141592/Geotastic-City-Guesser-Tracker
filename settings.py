import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3

connection = None
# Default settings sql injection
default_settings = """INSERT OR IGNORE INTO settings (setting, value) VALUES ('dark_mode', False), ('confirm_exit', True), ('confirm_delete', True), ('api_key', ''), ('rolling_number', 10)"""

def build_settings_frame(mainframe, apply_theme):
    header_label = ttk.Label(mainframe, text = "Settings:", font = ('Poppins',16))
    header_label.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    style = ttk.Style()
    style.configure("Custom.TCheckbutton", font = ('Poppins',12))

    mainframe.dark_mode_var = tk.BooleanVar(value = bool(int(read_setting('dark_mode'))))

    mainframe.confirm_exit_var = tk.BooleanVar(value = bool(int(read_setting('confirm_exit'))))

    mainframe.confirm_delete_var = tk.BooleanVar(value = bool(int(read_setting('confirm_delete'))))

    dark_mode_button = ttk.Checkbutton(mainframe, variable = mainframe.dark_mode_var, onvalue = True, offvalue = False, text = "Dark Mode", style = "Custom.TCheckbutton", command = lambda *args: modify_setting("dark_mode", mainframe.dark_mode_var.get(), apply_theme))

    dark_mode_button.grid(row = 1, column = 0, sticky = 'w', pady = 5, padx = 5)

    ask_exit_button = ttk.Checkbutton(mainframe, variable = mainframe.confirm_exit_var, onvalue = True, offvalue = False, text = "Confirm Exit", style = "Custom.TCheckbutton", command = lambda *args: modify_setting("confirm_exit", mainframe.confirm_exit_var.get(), apply_theme))

    ask_exit_button.grid(row = 2, column = 0, sticky = 'w', pady = 5, padx = 5)

    ask_delete_button = ttk.Checkbutton(mainframe, variable = mainframe.confirm_delete_var, onvalue = True, offvalue = False, text = "Confirm Delete", style = "Custom.TCheckbutton", command = lambda *args: modify_setting("confirm_delete", mainframe.confirm_delete_var.get(), apply_theme))

    ask_delete_button.grid(row = 3, column = 0, sticky = 'w', pady = 5, padx = 5)

    api_key_label = ttk.Label(mainframe, text = "Api Key: ", font = ('Poppins',11))
    api_key_label.grid(row = 4, column = 0, padx = 5, pady = 15, sticky = 'w')
    
    api_key_entry = ttk.Entry(mainframe, width = 30)
    api_key_entry.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 15)

    update_api_button = ttk.Button(mainframe, text = 'Update API', command = lambda *args: modify_setting("api_key", api_key_entry, apply_theme))
    update_api_button.grid(row = 4, column = 2, sticky = 'w', padx = 5, pady = 15)

    rolling_num_label = ttk.Label(mainframe, text = "Number of Rounds Shown: ", font = ('Poppins',11))
    rolling_num_label.grid(row = 5, column = 0, padx = 5, pady = 15, sticky = 'w')

    num_combo = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]
    rolling_combobox = ttk.Combobox(mainframe, value = num_combo, state = 'readonly')
    rolling_combobox.current(num_combo.index(int(read_setting('rolling_number'))))

    rolling_combobox.grid(row = 5, column = 1, padx = 5, pady = 15, sticky = 'w')

    



def modify_setting(setting, value, apply_theme):
    connection = sqlite3.connect('GT_settings.db')
    cursor = connection.cursor()

    if type(value) == ttk.Entry:
        temp_value = value.get()
        value.delete(0,END)
        value = temp_value

    if value == '':
        msgbox.showerror(title = 'Missing API Key', message = 'Textbox for API Key updating cannot be empty!')
        connection.commit()
        connection.close()
        return

    cursor.execute(f'UPDATE settings SET value = ? WHERE setting = ?', (value, setting))

    
    connection.commit()
    connection.close()

    

    apply_theme()

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

        if (value[0]) == '':
            return ''
        
    
        if setting == 'dark_mode' or setting == 'confirm_exit' or setting == 'confirm_delete':
            return bool(int(value[0]))
        else:
            return value[0]
    
    except sqlite3.OperationalError as error_code:
            print("Failed to read settings!", error_code)

    finally:
        connection.close()

def read_api():
    connection = sqlite3.connect("GT_settings.db")
    cursor = connection.cursor()

    try:
        read_setting = cursor.execute('SELECT value FROM settings WHERE setting = ?', ("api_key",))
        value = read_setting.fetchone()
    
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