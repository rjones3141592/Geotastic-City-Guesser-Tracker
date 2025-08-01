import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import stat_queries
import chart_creations


def build_insert_frame(mainframe):
    stat_tabs = ttk.Notebook(mainframe)

    overall_tab = ttk.Frame(stat_tabs)
    other_tab = ttk.Frame(stat_tabs)




    stat_tabs.add(overall_tab, text = 'Overall Stats')
    overall_build_insert_frame(overall_tab)
    stat_tabs.add(other_tab, text = 'Other Stats')

    stat_tabs.grid()

def overall_build_insert_frame(frame):
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

    value_label = ttk.Label(frame, text = 'Placeholder Value', font = ('Poppins',12))
    value_label.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_label = ttk.Label(frame, text = 'Placeholder Value', font = ('Poppins',12))
    value_label.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_label = ttk.Label(frame, text = 'Placeholder Value', font = ('Poppins',12))
    value_label.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)

    value_label = ttk.Label(frame, text = 'Placeholder Value', font = ('Poppins',12))
    value_label.grid(row = 4, column = 1, sticky = 'w', padx = 5, pady = 5)

    accuracy_values = stat_queries.count_correct_incorrect()

    accuracy_chart = chart_creations.percent_correct_pie(accuracy_values, frame)

    accuracy_chart.get_tk_widget().grid(row = 0, column = 99, padx = (300,0), pady = 0, rowspan = 7, sticky = 'e')

