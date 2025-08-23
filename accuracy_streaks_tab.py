import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

aas_tab = None

def build_insert_frame(frame):
    global aas_tab
    #aas -> accuracy and streaks
    aas_sub_header = ttk.Label(frame, text = "Accuracy & Streaks", font = ('Poppins',16))
    aas_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    overall_accuracy_label = ttk.Label(frame, text = 'Current Accuracy: ', font = ('Poppins',12))
    overall_accuracy_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5)

    overall_accuracy_label = ttk.Label(frame, text = 'Current Accuracy: ', font = ('Poppins',12))
    overall_accuracy_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5)

    value__accuracy_label = ttk.Label(frame, text = stat_queries.percent_accuracy() + '%', font = ('Poppins',12))
    value__accuracy_label.grid(row = 1, column = 1, sticky = 'w', padx = 5)

    aas_tab = frame
    refresh_line_plot()


def refresh_line_plot():
    global aas_tab
    # Empty_case check; no pie chart should be created
    if city_database.db_is_empty():
        return
    
    accuracy_list = stat_queries.rolling_round_accuracy(stat_queries.all_streaks())

    accuracy_line_plot, fig = chart_creations.rolling_average_line(accuracy_list)

    accuracy_line_plot = FigureCanvasTkAgg(fig, aas_tab)

    accuracy_line_plot.get_tk_widget().grid(row = 0, column = 2, pady = 0, rowspan = 6, sticky = 'e')