import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import settings
import data_insertion
import history_table
import display_statistics
import chart_creations
import import_file
import overall_tab
import accuracy_streaks_tab
import timing_tab
from tkinter import filedialog

# Ensures the database closes
def at_exit():
    if msgbox.askokcancel("Confirm Exit", "Do you want to exit the program?"):
        city_database.db_close()
        main.destroy()
        settings.settings_close()
    
# Modifies tab colors for dark mode
def apply_theme(dark_mode_val, style, main):
    if dark_mode_val == True:
        style.configure('.', background = '#121212', foreground = '#FFFFFF', highlightbackground = "#2A2A2E")
        style.configure('TEntry', fieldbackground = '#000000', foreground = '#FFFFFF')
        style.configure('TCombobox', fieldbackground = '#000000', selectbackground = '#000000', selectforeground = '#FFFFFF')
        style.configure('TNotebook.Tab', background = '#121212', foreground = '#FFFFFF')
        style.map('TNotebook.Tab', background = [('selected',"#252527"), ('!selected', '#121212'), ('active', '#252527')])
        style.map('TNotebook.Tab', foreground = [('selected','#636DF7'), ('!selected', '#FFFFFF')])
        style.map('TCombobox', fieldbackground = [('readonly','#000000')], selectbackground = [('readonly','#000000')], selectforeground = [('readonly','#FFFFFF')])
        main.option_add('*TCombobox*Listbox.background', '#000000')
        main.option_add('*TCombobox*Listbox.foreground', '#FFFFFF')
        main.option_add('*TCombobox*Listbox.selectbackground', '#FFFFFF')
        main.option_add('*TCombobox*Listbox.selectforeground', '#FFFFFF')
    else:
        style.configure('.', background = '#dcdad5', foreground = '#000000', highlightbackground = "#FFFFFF")
        style.configure('TEntry', fieldbackground = '#FFFFFF', foreground = '#000000')
        style.configure('TCombobox', fieldbackground = '#FFFFFF', selectbackground = '#FFFFFF', selectforeground = '#000000')
        style.configure('TNotebook.Tab', background = '#dcdad5', foreground = '#000000')
        style.map('TCombobox', fieldbackground = [('readonly','#FFFFFF')], selectbackground = [('readonly','#FFFFFF')], selectforeground = [('readonly','#000000')])
        style.map('TNotebook.Tab', foreground = [('selected','#636DF7'), ('!selected', '#000000')])
        style.map('TNotebook.Tab', background = [('selected','#FFFFFF'), ('!selected', '#dcdad5'), ('active', '#FFFFFF')])
        main.option_add('*TCombobox*Listbox.background', '#FFFFFF')
        main.option_add('*TCombobox*Listbox.foreground', '#000000')
        main.option_add('*TCombobox*Listbox.selectbackground', '#FFFFFF')
        main.option_add('*TCombobox*Listbox.selectforeground', '#000000')
    
    chart_creations.mpl_color()
    history_table.refresh_colors()
    overall_tab.refresh_pie_chart()
    accuracy_streaks_tab.refresh_histogram()
    accuracy_streaks_tab.refresh_line_plot()
    timing_tab.refresh_histogram()


# Establishing mainframe and sets up the notebook
main = tk.Tk()
main.title('City Streak Stat Tracker')
main_tab_frame = ttk.Notebook(main)

# Created 5 tabs for 5 aspects of program using a grid layout, initialized below.
import_data_tab = ttk.Frame(main_tab_frame)

insert_stat_tab = ttk.Frame(main_tab_frame)

guess_history_tab = ttk.Frame(main_tab_frame)

display_statistics_tab = ttk.Frame(main_tab_frame)

settings_tab = ttk.Frame(main_tab_frame)

main_tab_frame.add(insert_stat_tab, text = 'Data Entry')
data_insertion.build_insert_frame(insert_stat_tab)

main_tab_frame.add(guess_history_tab, text = 'Guess History')
history_table.build_insert_frame(guess_history_tab)

main_tab_frame.add(display_statistics_tab, text = 'Statistics')
display_statistics.build_insert_frame(display_statistics_tab)

# Modifying tab styling for design purposes
tab_style = ttk.Style()
tab_style.theme_use('clam')
apply_theme(settings.read_setting('dark_mode'), tab_style, main)

def apply_theme_settings():
    apply_theme(settings.read_setting('dark_mode'), tab_style, main)
tab_style.configure('TNotebook.Tab', font = ('Roboto',12))
tab_style.configure('TNotebook.Tab', padding = 5)

main_tab_frame.add(settings_tab, text = "Settings")
settings.build_settings_frame(settings_tab, apply_theme_settings)


main_tab_frame.grid()

city_database.db_startup()
settings.settings_startup()



main.protocol("WM_DELETE_WINDOW", at_exit)

main.resizable(width=False, height=False)

main.mainloop()

