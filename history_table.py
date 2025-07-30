import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import settings

def build_insert_frame(mainframe):
    tab_sub_header = ttk.Label(mainframe, text = "Guess History", font = ('Poppins',16))
    tab_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

    guess_table = ttk.Treeview(mainframe)

    guess_table['columns'] = ('id','g_city', 'g_st_ctry', 'correct', 't_city', 't_st_ctry', 'time', 'timestamp')

    # Configuring Styling
    style = ttk.Style()
    style.configure('Treeview.Heading', font = ('Poppins', 12))
    guess_table.tag_configure('oddrow', background = "#E6FAFF")
    guess_table.tag_configure('evenrow', background = "#FFFFFF")
    scrollbar = ttk.Scrollbar(mainframe, orient = 'vertical', command = guess_table.yview)
    scrollbar.grid(row = 1, column = 2, sticky = 'ns')

    guess_table.configure(yscrollcommand = scrollbar.set)

    # Establishing Column Sizes
    guess_table.column('#0', width = 0, stretch = tk.NO)
    guess_table.column('id', width = 0, stretch = tk.NO)
    guess_table.column('g_city', anchor = tk.W, width = 150)
    guess_table.column('g_st_ctry', anchor = tk.W, width = 150)
    guess_table.column('correct', anchor = tk.W, width = 75)
    guess_table.column('t_city', anchor = tk.W, width = 150)
    guess_table.column('t_st_ctry', anchor = tk.W, width = 150)
    guess_table.column('time', anchor = tk.W, width = 75)
    guess_table.column('timestamp', anchor = tk.W, width = 150)

    # Establishing Column headings
    guess_table.heading('g_city', text = 'Guess')
    guess_table.heading('g_st_ctry', text = 'State/Country')
    guess_table.heading('correct', text = 'Correct?')
    guess_table.heading('t_city', text = 'Target')
    guess_table.heading('t_st_ctry', text = 'State/Country')
    guess_table.heading('time', text = 'Time')
    guess_table.heading('timestamp', text = 'Date/Time')

    guess_table.grid(row = 1, column = 0, columnspan = 2)

    refresh_button = ttk.Button(mainframe, text = 'Refresh', command = lambda *args: refresh_data(guess_table))
    refresh_button.grid(row = 0, column = 1, sticky = 'e', padx = 5, pady = 5)

    delete_recent = ttk.Button(mainframe, text = 'Delete Recent', command = lambda *args: delete_most_recent(guess_table))
    delete_recent.grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 5)

    del_selected = ttk.Button(mainframe, text = 'Delete Selected', command = lambda *args: delete_selected(guess_table))
    del_selected.grid(row = 2, column = 1, sticky = 'e', padx = 5, pady = 5)

    refresh_data(guess_table)

def refresh_data(table):
    # Check if file exists
    if (city_database.db_exists() == False):
        return
    
    table.delete(*table.get_children())

    data = city_database.get_display_data()

    # Check if file has a table at all
    if (data == None):
        return
    

    for i, entry in enumerate(data):
        tag = 'oddrow'
        if (i % 2 == 0):
            tag = 'evenrow'
        
        table.insert(parent = '', index = 'end', values = entry, tags = (tag))


def delete_most_recent(table):
    if (settings.read_setting('confirm_delete')):
        if msgbox.askokcancel("Confirm Delete", "Are you sure you want to delete the most recent entry?"):
            city_database.db_remove_recent()
    else:
        city_database.db_remove_recent()

    
    refresh_data(table)

def delete_selected(table):
    selection = table.focus()
    
    if (selection == ''):
        msgbox.showerror(title = 'Missing Parameters', message = 'You must select a guess to delete!')
        return

    # Grabbing unique ID identifier for SQL usage purposes
    selection_values = table.item(selection)
    id = selection_values['values'][0]

    if (settings.read_setting('confirm_delete')):
        if msgbox.askokcancel("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            city_database.db_delete_selected(getint(id))

    else:
        city_database.db_delete_selected(getint(id))

    refresh_data(table)





    