import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def build_insert_frame(frame):
    aas_sub_header = ttk.Label(frame, text = "Cities", font = ('Poppins',16))
    aas_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    overall_accuracy_label = ttk.Label(frame, text = 'Most correctly guessed cities: ', font = ('Poppins',12))
    overall_accuracy_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5)

    query_label_correct = ttk.Label(frame, font = ('Poppins',10))

    most_correct = stat_queries.most_correct_cities()
    for entry in most_correct:
        percent_value = round(entry[0]*100,1)
        if (percent_value == 100):
            percent_value = round(int(percent_value))
        percent = str(percent_value) + '%'
        num_correct = str(entry[1])
        num_attempted = str(entry[2])
        city_name = entry[3]
        stc_name = entry[4]

        value_string = city_name + ', ' + stc_name + ' (' + num_correct + '/' + num_attempted + ', ' + percent + ')'

        print(value_string)

    most_incorrect = stat_queries.most_incorrect_cities()

    for entry in most_incorrect:
        percent_value = round(entry[0]*100,1)
        if (percent_value == 100 or percent_value == 0):
            percent_value = round(int(percent_value))
        percent = str(percent_value) + '%'
        num_correct = str(entry[1])
        num_attempted = str(entry[2])
        city_name = entry[3]
        stc_name = entry[4]

        value_string = city_name + ', ' + stc_name + ' (' + num_correct + '/' + num_attempted + ', ' + percent + ')'

        print(value_string)