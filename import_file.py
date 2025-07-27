import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox as msgbox

import requests
import logging
from time import sleep
import json
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

data = None

def build_insert_frame(mainframe):
    insert_file_button = ttk.Button(mainframe, text = 'Import JSON File', command = lambda *args: load_file())
    insert_file_button.grid(row = 0, column = 0, padx = 5, pady = 5)

def load_file():
    file_path = Path(filedialog.askopenfilename())

    if (file_path.suffix != '.json'):
        msgbox.showerror(title = 'Error in Import!', message = 'A non JSON file has been imported!')
        return
    
    else:
        pass

def api_calling():
    pass