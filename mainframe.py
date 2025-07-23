import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database
import settings
import insertion

# Defining Close function to ensure that database closes
def at_exit():
    if msgbox.askokcancel("Confirm Exit", "Do you want to exit the program?"):
        city_database.db_close()
        main.destroy()
        settings.settings_close()

# Establishing mainframe and sets up the notebook
main = tk.Tk()
main.title('City Streak Stat Tracker')
mainTabFrame = ttk.Notebook(main)

# Created 4 tabs for 4 aspects of program using a grid layout, initialized below.
insertStatTab = ttk.Frame(mainTabFrame)
insertStatTab.columnconfigure(0, weight = 1)
insertStatTab.columnconfigure(1, weight = 3)
for i in range(6):
    insertStatTab.rowconfigure(i, weight = 1)

recentData = ttk.Frame(mainTabFrame)
dataCorrect = ttk.Frame(mainTabFrame)
dataIncorrect = ttk.Frame(mainTabFrame)
settingsTab = ttk.Frame(mainTabFrame)

mainTabFrame.add(insertStatTab, text = 'Insert New Data')
insertion.build_insert_frame(insertStatTab)

mainTabFrame.add(recentData, text = 'Recent Submisssions')
mainTabFrame.add(dataCorrect, text = 'Correct City Stats')
mainTabFrame.add(dataIncorrect, text = 'Incorrect City Stats')


mainTabFrame.add(settingsTab, text = "Settings")
settings.build_settings_frame(settingsTab)


# Modifying tab styling
tabStyle = ttk.Style()
tabStyle.configure('TNotebook.Tab', font = ('Roboto',12))
tabStyle.configure('TNotebook.Tab', padding=5)


tabStyle.map('TNotebook.Tab', foreground = [('selected','#636DF7')])


mainTabFrame.grid()

city_database.db_startup()
settings.settings_startup()

main.protocol("WM_DELETE_WINDOW", at_exit)

main.mainloop()

