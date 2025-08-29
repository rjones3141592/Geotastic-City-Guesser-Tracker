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

    stat_queries.most_correct_cities()