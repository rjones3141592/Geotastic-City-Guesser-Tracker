from tkinter import *
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox as msgbox
import display_statistics
import read_json
import settings
import requests
import logging
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import history_table
data = None

logger = logging.getLogger(__name__)

REQUESTS_PER_SECOND = 5
GEOAPIFY_API_URL = "https://api.geoapify.com/v1/geocode/reverse"

def load_file():
    file_paths = filedialog.askopenfilenames(filetypes = [("JSON Files", "*.json")])

    if len(file_paths) == 0:
        return

    # Do nothing if no file was imported.
    for file_path in file_paths:
        if (Path(file_path).suffix == ''):
            return
        
        if (Path(file_path).suffix != '.json'):
            msgbox.showerror(title = 'Error in Import!', message = 'A non JSON file has been imported!')
            return
        
        coord_list = read_json.read_for_api_call(Path(file_path))

        api_list = batch_reverse(coord_list)

        read_json.read_for_db_input_auto(Path(file_path), api_list)

    msgbox.showinfo("Sucessful Input!", "Data successfully inputted into database!")

    history_table.refresh_data(history_table.order_parameters[history_table.order_combobox.get()][0], history_table.order_parameters[history_table.order_combobox.get()][1])
    display_statistics.refresh_all_data()

# This function is adapted from Geoapify's MIT-licensed sample code
# Source: https://www.geoapify.com/tutorial/reverse-geocoding-python/
# © 2025 Geoapify GmbH

def reverse_geocode(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'apiKey': settings.read_setting('api_key'),
        'format': 'json',
        'type': 'amenity'
    }
    try:
        response = requests.get(GEOAPIFY_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                return data['results'][0]
            elif 'features' in data:
                return data['features'][0]
            else:
                return {}
        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Too many requests.")
            return {}
        else:
            logger.error(f"Error: {response.status_code} for coordinates: ({lat}, {lon})")
            return {}
    except Exception as e:
        logger.error(f"Exception occurred: {e} for coordinates: ({lat}, {lon})")
        return {}

# This function is adapted from Geoapify's MIT-licensed sample code
# Source: https://www.geoapify.com/tutorial/reverse-geocoding-python/
# © 2025 Geoapify GmbH

def batch_reverse(batch_list):
    tasks = []

    with ThreadPoolExecutor(max_workers = 10) as executor:
        for batch in batch_list:
            logger.info(batch)

            coords = list(map(float, batch))

            tasks.append(executor.submit(reverse_geocode, coords[0], coords[1]))

            sleep(1)
    
    wait(tasks, return_when = ALL_COMPLETED)
    results = [task.result() for task in tasks]

    return results

