import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import overall_tab
import timing_tab

# Module level variables to allow refreshing of statistical data on the city tab

def build_insert_frame(mainframe):

    stat_tabs = ttk.Notebook(mainframe)

    overview_tab = ttk.Frame(stat_tabs)
    time_tab = ttk.Frame(stat_tabs)

    stat_tabs.add(overview_tab, text = 'Overview')
    overall_tab.build_insert_frame(overview_tab)
    stat_tabs.add(time_tab, text = 'Time')
    timing_tab.build_insert_frame(time_tab)

    stat_tabs.grid()

def refresh_all_data():
    overall_tab.refresh_labels()
    timing_tab.refresh_labels()

