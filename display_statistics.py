import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

overall_tab = None
# Module level variables to allow refreshing of statistical data
value_accuracy_label = None
value_time_label = None
value_streak_label = None
value_country_label = None

def build_insert_frame(mainframe):
    global overall_tab

    stat_tabs = ttk.Notebook(mainframe)

    overall_tab = ttk.Frame(stat_tabs)
    other_tab = ttk.Frame(stat_tabs)

    stat_tabs.add(overall_tab, text = 'Overall Stats')
    overall_build_insert_frame(overall_tab)
    stat_tabs.add(other_tab, text = 'Other Stats')

    stat_tabs.grid()

def overall_build_insert_frame(frame):
    global value_accuracy_label, value_country_label, value_streak_label, value_time_label

    overall_sub_header = ttk.Label(frame, text = "Stats Overview", font = ('Poppins',16))
    overall_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    accuracy_label = ttk.Label(frame, text = 'Accuracy of Guesses: ', font = ('Poppins',12))
    accuracy_label.grid(row = 1, column = 0, sticky = 'e', padx = 5, pady = 5)

    time_guess_label = ttk.Label(frame, text = 'Average Time of Guess: ', font = ('Poppins',12))
    time_guess_label.grid(row = 2, column = 0, sticky = 'e', padx = 5, pady = 5)

    streak_label = ttk.Label(frame, text = 'Longest Streak: ', font = ('Poppins',12))
    streak_label.grid(row = 3, column = 0, sticky = 'e', padx = 5, pady = 5)

    country_label = ttk.Label(frame, text = 'Most Played Country: ', font = ('Poppins',12))
    country_label.grid(row = 4, column = 0, sticky = 'e', padx = 5, pady = 5)

    value_accuracy_label = ttk.Label(frame, text = stat_queries.percent_accuracy(), font = ('Poppins',12))
    value_accuracy_label.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_time_label = ttk.Label(frame, text = stat_queries.average_time(), font = ('Poppins',12))
    value_time_label.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_streak_label = ttk.Label(frame, text = stat_queries.longest_streak(), font = ('Poppins',12))
    value_streak_label.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_country_label = ttk.Label(frame, text = 'Placeholder Value', font = ('Poppins',12))
    value_country_label.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

    refresh_pie_chart()

def refresh_labels():
    global value_accuracy_label, value_time_label, value_streak_label

    accuracy_value = stat_queries.percent_accuracy()
    avg_time = stat_queries.average_time()
    longest_streak = stat_queries.longest_streak()

    value_accuracy_label.config(text = accuracy_value)
    value_time_label.config(text = avg_time)
    value_streak_label.config(text = longest_streak)

    refresh_pie_chart()

def refresh_pie_chart():
    global overall_tab
    # Empty_case check; no pie chart should be created
    if city_database.db_is_empty():
        return
    
    accuracy_values = stat_queries.count_correct_incorrect()

    accuracy_chart, fig = chart_creations.percent_correct_pie(accuracy_values)

    accuracy_chart = FigureCanvasTkAgg(fig, overall_tab)

    accuracy_chart.get_tk_widget().grid(row = 0, column = 2, padx = (275,0), pady = 0, rowspan = 7, sticky = 'e')