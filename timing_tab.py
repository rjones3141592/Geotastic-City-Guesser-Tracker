import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def build_insert_frame(frame):
    timing_sub_header = ttk.Label(frame, text = "Time Stats", font = ('Poppins',16))
    timing_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)
    
    average_time_overall_label = ttk.Label(frame, text = 'Average Guess Time: ', font = ('Poppins',12))
    average_time_overall_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5, pady = 5)

    avg_time_correct_label = ttk.Label(frame, text = 'Average Time - Correct: ', font = ('Poppins',12))
    avg_time_correct_label.grid(row = 2, column = 0, sticky = 'w', padx = 15, pady = 5)

    avg_time_incorrect_label = ttk.Label(frame, text = 'Average Time - Incorrect: ', font = ('Poppins',12))
    avg_time_incorrect_label.grid(row = 3, column = 0, sticky = 'w', padx = 15, pady = 5)

    fastest_guess_label = ttk.Label(frame, text = 'Fastest correct guess: ', font = ('Poppins',12))
    fastest_guess_label.grid(row = 4, column = 0, sticky = 'ew', padx = 5, pady = 5)

    slowest_guess_label = ttk.Label(frame, text = 'Slowest correct guess: ', font = ('Poppins',12))
    slowest_guess_label.grid(row = 5, column = 0, sticky = 'ew', padx = 5, pady = 5)