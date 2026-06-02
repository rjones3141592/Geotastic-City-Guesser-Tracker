import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import settings
import stat_queries
import display_statistics

# Module level variable set to guess_table; allows Table to be refreshed when needed)
guess_table = None
edge_case_label = None

order_combobox = None
order_values = ['ID (newest)', 'ID (oldest)', 'Guess (A -> Z)', 'Guess (Z -> A)', 'Correct (Yes First)', 'Correct (No First)', 'Target (A -> Z)', 'Target (Z -> A)', 'Time (Fastest)', 'Time (Slowest)']
order_parameters = {'ID (newest)': ('id', 'DESC'), 'ID (oldest)': ('id', 'ASC'), 'Guess (A -> Z)': ('guessed_city', 'ASC'), 'Guess (Z -> A)': ('guessed_city', 'DESC'), 'Correct (Yes First)': ('correct_guess', 'DESC'), 'Correct (No First)': ('correct_guess', 'ASC'), 'Target (A -> Z)': ('correct_city', 'ASC'), 'Target (Z -> A)': ('correct_city', 'DESC'), 'Time (Fastest)': ('guess_time', 'ASC'), 'Time (Slowest)': ('guess_time', 'DESC')}

def build_insert_frame(mainframe):
    global edge_case_label, order_combobox
    tab_sub_header = ttk.Label(mainframe, text = "Guess History", font = ('Poppins',16))
    tab_sub_header.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = (0,5))

    edge_case_label = ttk.Label(mainframe, text = '* Same city guessed, but not close enough (outside radius)', font = ('Poppins', 8,'italic'))
    global guess_table
    guess_table = ttk.Treeview(mainframe)

    guess_table['columns'] = ('id','g_city', 'g_st_ctry', 'correct', 't_city', 't_st_ctry', 'time', 'timestamp')

    # Configuring Styling
    style = ttk.Style()
    style.configure('Treeview.Heading', font = ('Poppins', 12))
    if (settings.read_setting('dark_mode') == False):
        guess_table.tag_configure('oddrow', background = "#E6FAFF")
        guess_table.tag_configure('evenrow', background = "#FFFFFF")
    else:
        guess_table.tag_configure('oddrow', background = "#0E1729")
        guess_table.tag_configure('evenrow', background = "#000000")
    scrollbar = ttk.Scrollbar(mainframe, orient = 'vertical', command = guess_table.yview)
    scrollbar.grid(row = 2, column = 2, sticky = 'ns')

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

    order_combobox = ttk.Combobox(mainframe, value = order_values, state = 'readonly')
    order_combobox.current(0)
    order_combobox.grid(row = 1, column = 0, sticky = 'w', pady = (0,10), padx = (25,0))

    order_combobox.bind('<<ComboboxSelected>>', lambda x: refresh_data(order_parameters[order_combobox.get()][0], order_parameters[order_combobox.get()][1]))

    guess_table.grid(row = 2, column = 0, columnspan = 2, padx = (25,0))

    refresh_button = ttk.Button(mainframe, text = 'Refresh', command = lambda *args: refresh_data(order_parameters[order_combobox.get()][0], order_parameters[order_combobox.get()][1]))
    refresh_button.grid(row = 1, column = 1, sticky = 'e', padx = (25,0), pady = (0,10))

    delete_recent = ttk.Button(mainframe, text = 'Delete Recent', command = lambda *args: delete_most_recent())
    delete_recent.grid(row = 3, column = 0, sticky = 'w', padx = (25,0), pady = 10)

    del_selected = ttk.Button(mainframe, text = 'Delete Selected', command = lambda *args: delete_selected())
    del_selected.grid(row = 3, column = 1, sticky = 'e', pady = 10)

    guess_table.bind('<Double-1>', lambda event: onDoubleClick(event))

    refresh_data('id','DESC')

def refresh_colors():
    global guess_table
    if (settings.read_setting('dark_mode') == False):
        guess_table.tag_configure('oddrow', background = "#E6FAFF")
        guess_table.tag_configure('evenrow', background = "#FFFFFF")
    else:
        guess_table.tag_configure('oddrow', background = "#0E1729")
        guess_table.tag_configure('evenrow', background = "#000000")
def refresh_data(order, direction):
    global edge_case_label

    # Check if file exists
    if (city_database.db_exists() == False):
        return
    
    guess_table.delete(*guess_table.get_children())

    data = city_database.get_display_data(order, direction)[0]

    edge_case = city_database.get_display_data(order, direction)[1]
    
    if (edge_case):
        edge_case_label.grid(row = 4, column = 0, sticky = 'w', padx = (25,0))

    # Check if file has a table at all
    if (data == None):
        return
    

    for i, entry in enumerate(data):
        tag = 'oddrow'
        if (i % 2 == 0):
            tag = 'evenrow'
        
        guess_table.insert(parent = '', index = 'end', values = entry, tags = (tag))

    stat_queries.count_correct_incorrect()

def delete_most_recent():
    if (settings.read_setting('confirm_delete')):
        if msgbox.askokcancel("Confirm Delete", "Are you sure you want to delete the most recent entry?"):
            city_database.db_remove_recent()
    else:
        city_database.db_remove_recent()

    refresh_data(order_parameters[order_combobox.get()][0], order_parameters[order_combobox.get()][1])
    display_statistics.refresh_all_data()


def delete_selected():
    selection = guess_table.focus()
    
    if (selection == ''):
        msgbox.showerror(title = 'Missing Parameters', message = 'You must select a guess to delete!')
        return

    # Grabbing unique ID identifier for SQL usage purposes
    selection_values = guess_table.item(selection)
    id = selection_values['values'][0]

    if (settings.read_setting('confirm_delete')):
        if msgbox.askokcancel("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            city_database.db_delete_selected(getint(id))

    else:
        city_database.db_delete_selected(getint(id))

    refresh_data(order_parameters[order_combobox.get()][0], order_parameters[order_combobox.get()][1])
    display_statistics.refresh_all_data()

# Defining onDoubleClick for usage in editing treeview table (and sql database too)
def onDoubleClick(event):
    # Grabbing row to focus; checking if one exists
    selection = guess_table.focus()

    if (selection == ''):
        msgbox.showerror(title = 'Missing Parameters', message = 'You must select an entry in order to edit!')
        return

    popup = tk.Toplevel()
    popup.title('Update Values')

    selection_values = guess_table.item(selection)['values']

    current_guessed_city_label = ttk.Label(popup, text = 'Current Guessed City: ', font = ('Poppins',10))
    current_guessed_city_label.grid(row = 0, column = 0, sticky = 'w', pady = 5)

    value_current_guessed_city_label = ttk.Label(popup, text = selection_values[1] + ', ' + selection_values[2], font = ('Poppins',10))
    value_current_guessed_city_label.grid(row = 0, column = 1, sticky = 'w', pady = 5)

    current_target_city_label = ttk.Label(popup, text = 'Current Target City: ', font = ('Poppins',10))
    current_target_city_label.grid(row = 1, column = 0, sticky = 'w', pady = 5)

    value_current_target_city_label = ttk.Label(popup, text = selection_values[4] + ', ' + selection_values[5], font = ('Poppins',10))
    value_current_target_city_label.grid(row = 1, column = 1, sticky = 'w', pady = 5)

    blank_slate_label = ttk.Label(popup, font = ('Poppins',10))
    blank_slate_label.grid(row = 2, column = 0, sticky = 'ew')

    update_guessed_label = ttk.Label(popup, text = 'Update Guessed City: ', font = ('Poppins',10))
    update_guessed_label.grid(row = 3, column = 0, sticky = 'w', pady = 5)

    update_guessed_entry = ttk.Entry(popup, width = 40)
    update_guessed_entry.grid(row = 3, column = 1, sticky = 'ew', pady = 5)

    update_target_label = ttk.Label(popup, text = 'Update Target City: ', font = ('Poppins',10))
    
    update_target_entry = ttk.Entry(popup, width = 40)

    submit_button = ttk.Button(popup, text = 'Update Selected City', command = lambda *args: edit_values(popup, selection_values[0], selection_values[1], selection_values[4], selection_values[3], update_guessed_entry.get(), update_target_entry.get()))
    
    if (selection_values[3] == 'No'):
        update_target_label.grid(row = 4, column = 0, sticky = 'w', pady = 5)
        update_target_entry.grid(row = 4, column = 1, sticky = 'ew', pady = 5)

        submit_button.grid(row = 5, column = 1, sticky = 'n', pady = 5)

    else:
        update_guessed_label.config(text = 'Update Target City: ')
        submit_button.grid(row = 4, column = 1, sticky = 'n', pady = 5)



def edit_values(root, id, original_guessed, original_target, was_correct, guessed_city, target_city = ''):
    input_target = target_city
    input_guessed = guessed_city

    if (was_correct == 'Yes'):
        print('change')
        if guessed_city == '':
            input_guessed = original_guessed

        input_target = input_guessed
    
    elif was_correct == 'No':
        if input_guessed == '':
            input_guessed = original_guessed
        
        if input_target == '':
            input_target = original_target
    else:
        print('error!')
    
    print(input_target)

    city_database.db_edit_cities(id, input_guessed, input_target)

    root.destroy()

    refresh_data(order_parameters[order_combobox.get()][0], order_parameters[order_combobox.get()][1])
    display_statistics.refresh_all_data()
    