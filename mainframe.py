import tkinter as tk
from tkinter import ttk
from tkinter import *

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



main.mainloop()