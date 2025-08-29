import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import overall_tab
import timing_tab
import accuracy_streaks_tab
import city_statistics_tab

# Python file that congregates separate python tab files into one central file

def build_insert_frame(mainframe):

    stat_tabs = ttk.Notebook(mainframe)

    overview_tab = ttk.Frame(stat_tabs)
    time_tab = ttk.Frame(stat_tabs)
    acc_str_tab = ttk.Frame(stat_tabs)
    city_stats_tab = ttk.Frame(stat_tabs)

    stat_tabs.add(overview_tab, text = 'Overview')
    overall_tab.build_insert_frame(overview_tab)
    stat_tabs.add(time_tab, text = 'Time')
    timing_tab.build_insert_frame(time_tab)

    stat_tabs.add(acc_str_tab, text = 'Accuracy & Streaks')
    accuracy_streaks_tab.build_insert_frame(acc_str_tab)

    stat_tabs.add(city_stats_tab, text = 'Cities')
    city_statistics_tab.build_insert_frame(city_stats_tab)

    stat_tabs.grid()

def refresh_all_data():
    overall_tab.refresh_labels()
    timing_tab.refresh_labels()
    accuracy_streaks_tab.refresh_labels()

