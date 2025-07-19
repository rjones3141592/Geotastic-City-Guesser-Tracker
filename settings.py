import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3


def build_settings_frame(mainframe):
    label1 = ttk.Label(mainframe, text = "Settings!", justify = 'left', font = ('Poppins',15))
    label1.configure()

    label1.pack(pady=10, padx = 5, anchor = 'w')

def settings_startup():
    global connection
    # Creating file
    db_file = "GTSettings.db"

    # SQL Statement on table creation
    settings_table = """CREATE TABLE IF NOT EXISTS settings (
        darkmode BOOLEAN PRIMARY KEY,
        confirmExit BOOLEAN NOT NULL,
        confirmDelete BOOLEAN NOT NULL
    );"""

    # Try except to catch any issues with starting SQL connection
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Another try except, this time for table creation
        try:
            cursor.execute(settings_table)
            connection.commit()
            
            print("Settings successfully created!")
        except sqlite3.OperationalError as error_code:
            print("Failed to create settings! Error code: ", error_code)

    except sqlite3.OperationalError as error_code:
        print("Failed to open settings! Error Code: ", error_code)



def settings_close():
    global connection
    if connection:
        connection.close()
        print("Successfully closed settings!")