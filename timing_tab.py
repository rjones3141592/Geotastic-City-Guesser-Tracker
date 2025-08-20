import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Module level variables to allow refreshing of statistical data on the overall tab
timing_tab = None
value_average_time_label = None
value_correct_time_label = None
value_incorrect_time_label = None
value_fastest_guess_label = None
value_slowest_guess_label = None

def build_insert_frame(frame):
    global timing_tab, value_average_time_label, value_correct_time_label, value_incorrect_time_label, value_fastest_guess_label, value_slowest_guess_label

    timing_sub_header = ttk.Label(frame, text = "Time Stats", font = ('Poppins',16))
    timing_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)
    
    average_time_overall_label = ttk.Label(frame, text = 'Average Guess Time: ', font = ('Poppins',12))
    average_time_overall_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5)

    avg_time_correct_label = ttk.Label(frame, text = 'Average Time - Correct: ', font = ('Poppins',12))
    avg_time_correct_label.grid(row = 2, column = 0, sticky = 'e', padx = 20)

    avg_time_incorrect_label = ttk.Label(frame, text = 'Average Time - Incorrect: ', font = ('Poppins',12))
    avg_time_incorrect_label.grid(row = 3, column = 0, sticky = 'e', padx = 20)

    fastest_guess_label = ttk.Label(frame, text = 'Fastest correct guess: ', font = ('Poppins',12))
    fastest_guess_label.grid(row = 4, column = 0, sticky = 'ew', padx = 5)

    slowest_guess_label = ttk.Label(frame, text = 'Slowest correct guess: ', font = ('Poppins',12))
    slowest_guess_label.grid(row = 5, column = 0, sticky = 'ew', padx = 5)

    value_average_time_label = ttk.Label(frame, text = stat_queries.average_time(), font = ('Poppins',12))
    value_average_time_label.grid(row = 1, column = 1, sticky = 'w', padx = 5)

    value_correct_time_label = ttk.Label(frame, text = stat_queries.average_times_correct_incorrect()[0], font = ('Poppins',12))
    value_correct_time_label.grid(row = 2, column = 1, sticky = 'w', padx = 5)

    value_incorrect_time_label = ttk.Label(frame, text = stat_queries.average_times_correct_incorrect()[1], font = ('Poppins',12))
    value_incorrect_time_label.grid(row = 3, column = 1, sticky = 'w', padx = 5)

    value_fastest_guess_label = ttk.Label(frame, text = stat_queries.fastest_slowest_correct_time()[0], font = ('Poppins',12))
    value_fastest_guess_label.grid(row = 4, column = 1, sticky = 'w', padx = 5)

    value_slowest_guess_label = ttk.Label(frame, text = stat_queries.fastest_slowest_correct_time()[1], font = ('Poppins',12))
    value_slowest_guess_label.grid(row = 5, column = 1, sticky = 'w', padx = 5)

    timing_tab = frame
    print(stat_queries.accuracy_rolling_average())
    refresh_histogram()

# refreshes labels in time stats tab following any database updates
def refresh_labels():
    global value_average_time_label, value_correct_time_label, value_incorrect_time_label, value_fastest_guess_label, value_slowest_guess_label
    
    average_time = stat_queries.average_time()
    avg_correct_time = stat_queries.average_times_correct_incorrect()[0]
    avg_incorrect_time = stat_queries.average_times_correct_incorrect()[1]
    fastest_time = stat_queries.fastest_slowest_correct_time()[0]
    slowest_time = stat_queries.fastest_slowest_correct_time()[1]

    value_average_time_label.config(text = average_time)
    value_correct_time_label.config(text = avg_correct_time)
    value_incorrect_time_label.config(text = avg_incorrect_time)
    value_fastest_guess_label.config(text = fastest_time)
    value_slowest_guess_label.config(text = slowest_time)

    refresh_histogram()

def refresh_histogram():
    global timing_tab
    # Empty_case check; no pie chart should be created
    if city_database.db_is_empty():
        return
    
    timing_values = stat_queries.times_for_correct_incorrect()

    timing_histogram, fig = chart_creations.time_histogram(timing_values)

    timing_histogram = FigureCanvasTkAgg(fig, timing_tab)

    timing_histogram.get_tk_widget().grid(row = 0, column = 2, pady = 0, rowspan = 6, sticky = 'e')