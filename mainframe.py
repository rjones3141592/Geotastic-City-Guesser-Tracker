import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import settings
import data_insertion
import history_table
import display_statistics
import import_file
from tkinter import filedialog

# Ensures the database closes
def at_exit():
    if msgbox.askokcancel("Confirm Exit", "Do you want to exit the program?"):
        city_database.db_close()
        main.destroy()
        settings.settings_close()

# Establishing mainframe and sets up the notebook
main = tk.Tk()
main.title('City Streak Stat Tracker')
main_tab_frame = ttk.Notebook(main)

# Created 5 tabs for 5 aspects of program using a grid layout, initialized below.
import_data_tab = ttk.Frame(main_tab_frame)

insert_stat_tab = ttk.Frame(main_tab_frame)
insert_stat_tab.columnconfigure(0, weight = 0)
insert_stat_tab.columnconfigure(1, weight = 0)
insert_stat_tab.columnconfigure(2, weight = 0)
insert_stat_tab.columnconfigure(3, weight = 0)
for i in range(8):
    insert_stat_tab.rowconfigure(i, weight = 0)

guess_history_tab = ttk.Frame(main_tab_frame)
for j in range(2):
    guess_history_tab.columnconfigure(j, weight = 2)

guess_history_tab.rowconfigure(0, weight = 0)
guess_history_tab.rowconfigure(1, weight = 0)
guess_history_tab.rowconfigure(2, weight = 0)
guess_history_tab.rowconfigure(3, weight = 0)

display_statistics_tab = ttk.Frame(main_tab_frame)

settings_tab = ttk.Frame(main_tab_frame)
settings_tab.rowconfigure(0, weight = 1)
settings_tab.rowconfigure(1, weight = 2)

main_tab_frame.add(insert_stat_tab, text = 'Data Entry')
data_insertion.build_insert_frame(insert_stat_tab)

main_tab_frame.add(guess_history_tab, text = 'Guess History')
history_table.build_insert_frame(guess_history_tab)

main_tab_frame.add(display_statistics_tab, text = 'Statistics')
display_statistics.build_insert_frame(display_statistics_tab)

main_tab_frame.add(settings_tab, text = "Settings")
settings.build_settings_frame(settings_tab)


# Modifying tab styling for design purposes
tab_style = ttk.Style()
tab_style.configure('TNotebook.Tab', font = ('Roboto',12))
tab_style.configure('TNotebook.Tab', padding=5)

tab_style.map('TNotebook.Tab', foreground = [('selected','#636DF7')])

main_tab_frame.grid()

city_database.db_startup()
settings.settings_startup()

main.protocol("WM_DELETE_WINDOW", at_exit)

main.resizable(width=False, height=False)

main.mainloop()

