import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import sqlite3
import city_database

def build_insert_frame(mainframe):
    # Setting up GUI layout of insertion tab
    tab_label = ttk.Label(mainframe, text = "Insert recent guess here. format it to be City, State or City, Country", font = ('Poppins',12))
    tab_label.grid(row = 0, column = 1, sticky = 'ew', padx = 5, pady = 5)

    guessed_city_label = ttk.Label(mainframe, text = "Guessed city: ", font = ('Poppins',11))
    guessed_city_label.grid(row = 1, column = 0, padx = 5, pady = 5)

    guessed_city_entry = ttk.Entry(mainframe, width = 30)
    guessed_city_entry.grid(row = 1, column = 1, sticky = 'ew', padx = 5, pady = 5)

    guessed_stc_label = ttk.Label(mainframe, text = 'State/Country: ', font = ('Poppins', 11))
    guessed_stc_label.grid(row = 1, column = 2, padx = 5, pady = 5)

    guessed_state_country = ttk.Entry(mainframe, width = 15)
    guessed_state_country.grid(row = 1, column = 3, sticky = 'ew', padx = 5, pady = 5)

    correct_label = ttk.Label(mainframe, text = 'Was it correct?', font = ('Poppins', 11))
    correct_label.grid(row = 2, column = 0, padx = 5, pady = 5)

    # Default selection for "was it correct" will be True.
    correct_var = tk.BooleanVar(value = True)

    wasCorrect = ttk.Checkbutton(mainframe, variable = correct_var, onvalue = True, offvalue = False, command = lambda *args: hide_show_correct_city(correct_var, answer_city_label, answer_city_entry, answer_stc_label, answer_stc_entry, submit_button, time_guess_label, time_guess_entry))
    wasCorrect.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    # Establishing 'correct' city answer and state/country; will need to hide for only when was_correct was unchecked.
    answer_city_label = ttk.Label(mainframe, text = 'Correct City:', font = ('Poppins', 11))

    answer_city_entry = ttk.Entry(mainframe, width = 30)

    answer_stc_label = ttk.Label(mainframe, text = 'State/Country: ', font = ('Poppins', 11))

    answer_stc_entry = ttk.Entry(mainframe, width = 15)

    time_guess_label = ttk.Label(mainframe, text = 'Time Taken (optional): ', font = ('Poppins',11))
    time_guess_label.grid(row = 3, column = 0, padx = 5, pady = 5)

    time_guess_entry = ttk.Entry(mainframe, width = 15)
    time_guess_entry.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)

    # Button to submit the query
    submit_button = ttk.Button(mainframe, text = 'Insert Guess', command = lambda *args: submitting_attempt(guessed_city_entry, guessed_state_country, correct_var, answer_city_entry, answer_stc_entry, time_guess_entry))
    submit_button.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

# Grabs values to submit into SQL database before clearing entries
def submitting_attempt(guessed_city, guessed_stc, correct_boolean, actual_city = None, actual_state_country = None, time = None):
    guessed_city_value = guessed_city.get()
    guessed_stc_value = guessed_stc.get()
    correct = correct_boolean.get()
    if (correct):
        actual_city_value = guessed_city_value
        actual_state_country_value = guessed_stc_value
    else:
        actual_city_value = actual_city.get()
        actual_state_country_value = actual_state_country.get()

    time_value = None

    # Checking for empty inputs
    if (guessed_city_value == '' or guessed_stc_value == ''):
        msgbox.showerror(title = 'Missing Parameters', message = 'Input fields cannot be empty!')
        return
    
    if (correct == False):
        if (actual_city_value == '' or actual_state_country_value == ''):
            msgbox.showerror(title = 'Missing Parameters', message = 'Input fields cannot be empty!')
            return

    # Converting time to float, catching error in case anything other than numbers is entered
    # Only done if time is not None
    if (time.get() != ''):
        try:
            time_value = float(time.get().strip())
        except ValueError as error_code:
            print("Failed to get time. Error code: ", error_code)
            msgbox.showerror(title = 'Invalid Time Entry!', message = 'Invalid time has been entered!')
            return 

        if (time_value <= 0):
            msgbox.showerror(title = 'Invalid Time Entry', message = 'Time must be greater than 0')
            return
        
        time.delete(0,END)

    guessed_city.delete(0,END)
    guessed_stc.delete(0,END)
    actual_city.delete(0,END)
    actual_state_country.delete(0,END)

    city_database.db_add(guessed_city_value, guessed_stc_value, correct, actual_city_value, actual_state_country_value, time_value)

# Hides and shows manual input's incorrect city.
def hide_show_correct_city(checkbox_status, ans_city_label, ans_city_entry, ans_stc_label, ans_stc_entry, submit_button, time_label, time_entry):
    if (checkbox_status.get()): # Onvalue is True
        ans_city_label.grid_remove()
        ans_city_entry.grid_remove()
        ans_stc_label.grid_remove()
        ans_stc_entry.grid_remove()

        submit_button.grid_remove()
        submit_button.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

        time_label.grid_remove()
        time_label.grid(row = 3, column = 0, padx = 5, pady = 5)

        time_entry.grid_remove()
        time_entry.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)
    else:
        ans_city_label.grid(row = 3, column = 0, padx = 5, pady = 5)
        ans_city_entry.grid(row = 3, column = 1, sticky = 'ew', padx = 5, pady = 5)
        ans_stc_label.grid(row = 3, column = 2, padx = 5, pady = 5)
        ans_stc_entry.grid(row = 3, column = 3, sticky = 'ew', padx = 5, pady = 5)

        submit_button.grid_remove()
        submit_button.grid(row = 5, column = 1, sticky = 'w', padx = 5, pady = 5)

        time_label.grid_remove()
        time_label.grid(row = 4, column = 0, padx = 5, pady = 5)

        time_entry.grid_remove()
        time_entry.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

    