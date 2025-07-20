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

    was_correct = ttk.Checkbutton(mainframe, variable = correct_var)
    was_correct.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    # Establishing 'correct' city answer; will need to hide for only when was_correct was unchecked.
    answer_label = ttk.Label(mainframe, text = 'Correct City:', font = ('Poppins', 11))
    answer_label.grid(row = 3, column = 0, padx = 5, pady = 5)

    answer_entry = ttk.Entry(mainframe, width = 30)
    answer_entry.grid(row = 3, column = 1, sticky = 'ew', padx = 5, pady = 5)

    
    