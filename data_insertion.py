import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox

import read_json
import requests
import settings
import import_file
import history_table
import display_statistics

REQUESTS_PER_SECOND = 5
GEOAPIFY_API_URL = "https://api.geoapify.com/v1/geocode/search"

def build_insert_frame(mainframe):
    # Setting up GUI layout of insertion tab
    tab_label = ttk.Label(mainframe, text = "Insert recent guess here. Format it to be City, State or City, Country", font = ('Poppins',12))
    tab_label.grid(row = 0, column = 1, sticky = 'ew', padx = 5, pady = 15)

    guessed_city_label = ttk.Label(mainframe, text = "Guessed City:", font = ('Poppins',11))
    guessed_city_label.grid(row = 1, column = 0, padx = 5, pady = 15, sticky = 'e')

    guessed_city_entry = ttk.Entry(mainframe, width = 30)
    guessed_city_entry.grid(row = 1, column = 1, sticky = 'ew', padx = 5, pady = 15)

    guessed_stc_label = ttk.Label(mainframe, text = 'State/Country:', font = ('Poppins', 11))
    guessed_stc_label.grid(row = 1, column = 2, padx = 5, pady = 15)

    guessed_state_country = ttk.Entry(mainframe, width = 15)
    guessed_state_country.grid(row = 1, column = 3, sticky = 'ew', padx = 5, pady = 15)

    correct_label = ttk.Label(mainframe, text = 'Was it correct?', font = ('Poppins', 11))
    correct_label.grid(row = 2, column = 0, padx = 5, pady = 15, sticky = 'e')

    # Default selection for "was it correct" will be True.
    correct_var = tk.BooleanVar(value = True)

    wasCorrect = ttk.Checkbutton(mainframe, variable = correct_var, onvalue = True, offvalue = False, command = lambda *args: hide_show_correct_city(correct_var, answer_city_label, answer_city_entry, answer_stc_label, answer_stc_entry, submit_button, time_guess_label, time_guess_entry))
    wasCorrect.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    # Establishing 'correct' city answer and state/country; will need to hide for only when was_correct was unchecked.
    answer_city_label = ttk.Label(mainframe, text = 'Correct City:', font = ('Poppins', 11))

    answer_city_entry = ttk.Entry(mainframe, width = 30)

    answer_stc_label = ttk.Label(mainframe, text = 'State/Country:', font = ('Poppins', 11))

    answer_stc_entry = ttk.Entry(mainframe, width = 15)

    time_guess_label = ttk.Label(mainframe, text = 'Time Taken (optional):', font = ('Poppins',11))
    time_guess_label.grid(row = 3, column = 0, padx = 5, pady = 15)

    time_guess_entry = ttk.Entry(mainframe, width = 15)
    time_guess_entry.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 15)

    # Button to submit the query
    submit_button = ttk.Button(mainframe, text = 'Insert Guess', command = lambda *args: submitting_attempt(guessed_city_entry, guessed_state_country, correct_var, answer_city_entry, answer_stc_entry, time_guess_entry))
    submit_button.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 15)

    # Stuff for importation
    insert_file_button = ttk.Button(mainframe, text = 'Import JSON File', command = lambda *args: import_file.load_file())
    insert_file_button.grid(row = 0, column = 0, padx = 5, pady = 15)

# Grabs values to submit into SQL database before clearing entries
def submitting_attempt(guessed_city, guessed_stc, correct_boolean, actual_city = None, actual_state_country = None, time = None):
    guess_api = None
    actual_api = None

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

    guess_api = geocode_search(guessed_city_value, guessed_stc_value)

    if (not correct):
        actual_api = geocode_search(actual_city_value, actual_state_country_value)

    read_json.read_for_db_input_manual(guess_api, correct_boolean.get(), actual_api, time_value)

    msgbox.showinfo("Sucessful Input!", "Data successfully inputted into database!")

    history_table.refresh_data()
    display_statistics.refresh_labels()

    

# Hides and shows manual input's incorrect city.
def hide_show_correct_city(checkbox_status, ans_city_label, ans_city_entry, ans_stc_label, ans_stc_entry, submit_button, time_label, time_entry):
    if (checkbox_status.get()): # Onvalue is True
        ans_city_label.grid_remove()
        ans_city_entry.grid_remove()
        ans_stc_label.grid_remove()
        ans_stc_entry.grid_remove()

        submit_button.grid_remove()
        submit_button.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 15)

        time_label.grid_remove()
        time_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'e')

        time_entry.grid_remove()
        time_entry.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 15)
    else:
        ans_city_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'e')
        ans_city_entry.grid(row = 3, column = 1, sticky = 'ew', padx = 5, pady = 15)
        ans_stc_label.grid(row = 3, column = 2, padx = 5, pady = 5)
        ans_stc_entry.grid(row = 3, column = 3, sticky = 'ew', padx = 5, pady = 15)

        submit_button.grid_remove()
        submit_button.grid(row = 5, column = 1, sticky = 'w', padx = 5, pady = 15)

        time_label.grid_remove()
        time_label.grid(row = 4, column = 0, padx = 5, pady = 15, sticky = 'e')

        time_entry.grid_remove()
        time_entry.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 15)

# This function is adapted from Geoapify's MIT-licensed sample code
# Source: https://www.geoapify.com/tutorial/reverse-geocoding-python/
# © 2025 Geoapify GmbH

def geocode_search(city, country):
    params = {
        'text': city + ', ' + country,
        'apiKey': settings.read_setting('api_key'),
        'format': 'json',
        'type': 'city'
    }

    output = requests.get(url = GEOAPIFY_API_URL, params = params)
    
    data = output.json()

    return data
