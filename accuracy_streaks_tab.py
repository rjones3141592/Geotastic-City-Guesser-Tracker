import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

aas_tab = None
value_accuracy_label = None
value_avg_streak_label = None
value_longest_streak_label = None

def build_insert_frame(frame):
    frame.grid_columnconfigure(2, weight = 2)
    global aas_tab, value_accuracy_label, value_avg_streak_label, value_longest_streak_label
    #aas -> accuracy and streaks
    aas_sub_header = ttk.Label(frame, text = "Accuracy & Streaks", font = ('Poppins',16))
    aas_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    overall_accuracy_label = ttk.Label(frame, text = 'Overall Accuracy: ', font = ('Poppins',12))
    overall_accuracy_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5)

    value_accuracy_label = ttk.Label(frame, text = stat_queries.percent_accuracy() + '%', font = ('Poppins',12))
    value_accuracy_label.grid(row = 1, column = 1, sticky = 'w', padx = 5)

    average_streak_label = ttk.Label(frame, text = 'Average Streak Length: ', font = ('Poppins',12))
    average_streak_label.grid(row = 2, column = 0, sticky = 'ew', padx = 5)

    value_avg_streak_label = ttk.Label(frame, text = stat_queries.average_streaks(), font = ('Poppins',12))
    value_avg_streak_label.grid(row = 2, column = 1, sticky = 'w', padx = 5)

    longest_streak_label = ttk.Label(frame, text = 'Longest Streak: ', font = ('Poppins',12))
    longest_streak_label.grid(row = 3, column = 0, sticky = 'ew', padx = 5)

    value_longest_streak_label = ttk.Label(frame, text = stat_queries.longest_streak(), font = ('Poppins',12))
    value_longest_streak_label.grid(row = 3, column = 1, sticky = 'ew', padx = 5)

    recent_accuracy_button = ttk.Button(frame, text = 'Show Recent Accuracy', command = lambda *args: refresh_line_plot())
    recent_accuracy_button.grid(row = 4, column = 0, padx = 10, sticky = 'e')

    streaks_histogram_button = ttk.Button(frame, text = 'Show Streaks Histogram', command = lambda *args: refresh_histogram())
    streaks_histogram_button.grid(row = 5, column = 0, sticky = 'e', padx = 10)
    
    aas_tab = frame
    refresh_line_plot()

def refresh_labels():
    global value_accuracy_label, value_avg_streak_label, value_longest_streak_label

    value_accuracy = stat_queries.percent_accuracy() + '%'
    average_streak = stat_queries.average_streaks()
    longest_streak = stat_queries.longest_streak()

    value_accuracy_label.config(text = value_accuracy)
    value_avg_streak_label.config(text = average_streak)
    value_longest_streak_label.config(text = longest_streak)

    refresh_line_plot()

def refresh_line_plot():
    global aas_tab
    # Empty_case check; no pie chart should be created
    if city_database.db_is_empty():
        return
    
    accuracy_list = stat_queries.rolling_round_accuracy()

    accuracy_line_plot, fig = chart_creations.rolling_average_line(accuracy_list)

    accuracy_line_plot = FigureCanvasTkAgg(fig, aas_tab)

    accuracy_line_plot.get_tk_widget().grid(row = 0, column = 2, pady = 0, rowspan = 6, sticky = 'e', padx = (255,0))

def refresh_histogram():
    global aas_tab
    # Empty_case check; no pie chart should be created
    if city_database.db_is_empty():
        return
    
    streaks_list = stat_queries.all_streaks()

    streaks_histogram, fig = chart_creations.streaks_histogram(streaks_list)

    streaks_histogram = FigureCanvasTkAgg(fig, aas_tab)

    streaks_histogram.get_tk_widget().grid(row = 0, column = 2, pady = 0, rowspan = 6, sticky = 'e', padx = (255,0))