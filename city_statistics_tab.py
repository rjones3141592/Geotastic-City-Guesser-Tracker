import tkinter as tk
from tkinter import ttk
import stat_queries
import city_database
import stat_queries
import chart_creations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

correct_labels = None
incorrect_labels = None

def build_insert_frame(frame):
    global correct_labels, incorrect_labels

    aas_sub_header = ttk.Label(frame, text = "Cities", font = ('Poppins',16))
    aas_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 10)

    overall_accuracy_label = ttk.Label(frame, text = 'Most correctly guessed cities: ', font = ('Poppins',12))
    overall_accuracy_label.grid(row = 1, column = 0, sticky = 'ew', padx = 5, pady = 5)

    overall_inaccuracy_label = ttk.Label(frame, text = 'Most incorrectly guessed cities: ', font = ('Poppins',12))
    overall_inaccuracy_label.grid(row = 1, column = 1, sticky = 'ew', padx = 20, pady = 5)

    query_label_correct_1 = ttk.Label(frame, font = ('Poppins',12))
    query_label_correct_2 = ttk.Label(frame, font = ('Poppins',12))
    query_label_correct_3 = ttk.Label(frame, font = ('Poppins',12))
    query_label_correct_4 = ttk.Label(frame, font = ('Poppins',12))
    query_label_correct_5 = ttk.Label(frame, font = ('Poppins',12))

    query_label_incorrect_1 = ttk.Label(frame, font = ('Poppins',12))
    query_label_incorrect_2 = ttk.Label(frame, font = ('Poppins',12))
    query_label_incorrect_3 = ttk.Label(frame, font = ('Poppins',12))
    query_label_incorrect_4 = ttk.Label(frame, font = ('Poppins',12))
    query_label_incorrect_5 = ttk.Label(frame, font = ('Poppins',12))

    correct_labels = [query_label_correct_1, query_label_correct_2, query_label_correct_3, query_label_correct_4, query_label_correct_5]
    incorrect_labels = [query_label_incorrect_1, query_label_incorrect_2, query_label_incorrect_3, query_label_incorrect_4, query_label_incorrect_5]
    
    refresh_lists()

def refresh_lists():
    global correct_labels, incorrect_labels

    most_correct = stat_queries.most_correct_cities()
    i = 1

    value_corrects = []
    value_incorrects = []

    for entry in most_correct:
        percent_value = round(entry[0]*100,1)
        if (percent_value == 100):
            percent_value = round(int(percent_value))
        percent = str(percent_value) + '%'
        num_correct = str(entry[1])
        num_attempted = str(entry[2])
        city_name = entry[3]
        stc_name = entry[4]

        value_corrects.append(str(i) + '. ' + city_name + ', ' + stc_name + ' (' + num_correct + '/' + num_attempted + ', ' + percent + ')')

        i += 1

    i = 1

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

        value_incorrects.append(str(i) + '. ' + city_name + ', ' + stc_name + ' (' + num_correct + '/' + num_attempted + ', ' + percent + ')')

        i += 1

    i = 0

    while i in range(len(value_corrects)):
        correct_labels[i].config(text = value_corrects[i])

        correct_labels[i].grid(row = i + 2, column = 0, sticky = 'w', padx = 10, pady = 10)

        i += 1

    i = 0

    while i in range(len(value_incorrects)):
        incorrect_labels[i].config(text = value_incorrects[i])

        incorrect_labels[i].grid(row = i + 2, column = 1, sticky = 'w', padx = 30, pady = 10)

        i += 1