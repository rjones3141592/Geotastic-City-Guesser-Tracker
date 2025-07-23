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

    guessed_label = ttk.Label(mainframe, text = "Guessed City: ", font = ('Poppins',11))
    guessed_label.grid(row = 1, column = 0, padx = 5, pady = 5)

    guessed_entry = ttk.Entry(mainframe, width = 30)
    guessed_entry.grid(row = 1, column = 1, sticky = 'ew', padx = 5, pady = 5)

    correct_label = ttk.Label(mainframe, text = 'Was it correct?', font = ('Poppins', 11))
    correct_label.grid(row = 2, column = 0, padx = 5, pady = 5)

    # Default selection for "was it correct" will be True.
    correct_var = tk.BooleanVar(value = True)

    was_correct = ttk.Checkbutton(mainframe, variable = correct_var, onvalue = True, offvalue = False, command = lambda *args: hide_show_correct_city(correct_var, answer_label, answer_entry, submit_button))
    was_correct.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    # Establishing 'correct' city answer; will need to hide for only when was_correct was unchecked.
    answer_label = ttk.Label(mainframe, text = 'Correct City:', font = ('Poppins', 11))

    answer_entry = ttk.Entry(mainframe, width = 30)

    # Button to submit the query
    submit_button = ttk.Button(mainframe, text = 'Insert Attempt!', command = lambda *args: submitting_attempt(guessed_entry, correct_var, answer_entry))
    submit_button.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)

    return guessed_entry, correct_var, answer_label, answer_entry, submit_button

# Grabs values to submit into SQL database before clearing entries
def submitting_attempt(guessed_city, correct_boolean, actual_city):
    guess = guessed_city.get()
    guessed_city.delete(0, 'end')

    correct = correct_boolean.get()

    actual = actual_city.get()
    actual_city.delete(0, 'end')

    city_database.db_add(guess, correct, actual)


def hide_show_correct_city(checkbox_status, ans_label, ans_entry, submit_button):
    if (checkbox_status.get()): # Onvalue is True
        ans_label.grid_remove()
        ans_entry.grid_remove()

        submit_button.grid_remove()
        submit_button.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)
    else:
        ans_label.grid(row = 3, column = 0, padx = 5, pady = 5)
        ans_entry.grid(row = 3, column = 1, sticky = 'ew', padx = 5, pady = 5)
        submit_button.grid_remove()
        submit_button.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

    