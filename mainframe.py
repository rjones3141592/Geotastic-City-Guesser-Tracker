import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msgbox
import city_database

# Defining Close function to ensure that database closes
def at_exit():
    if msgbox.askokcancel("Confirm Exit", "Do you want to exit the program?"):
        city_database.db_close()
        main.destroy()


# Establishing main
main = tk.Tk()
main.title('City Streak Stat Tracker')

# Setting up Frames via a Notebook Widget
mainTabFrame = ttk.Notebook(main)

# Created 4 tabs for 4 aspects of program
insertStatTab = ttk.Frame(mainTabFrame)
recentData = ttk.Frame(mainTabFrame)
dataCorrect = ttk.Frame(mainTabFrame)
dataIncorrect = ttk.Frame(mainTabFrame)

mainTabFrame.add(insertStatTab, text = 'Insert New Data')
mainTabFrame.add(recentData, text = 'Recent Submisssions')
mainTabFrame.add(dataCorrect, text = 'Correct City Stats')
mainTabFrame.add(dataIncorrect, text = 'Incorrect City Stats')

mainTabFrame.pack(expand=1, fill='y')

city_database.db_startup()

main.protocol("WM_DELETE_WINDOW", at_exit)

main.mainloop()

