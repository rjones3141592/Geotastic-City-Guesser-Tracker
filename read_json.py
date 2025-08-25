import json
import city_database
import history_table

# Exports list in [lat, lon] format of list
def read_for_api_call(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)

    batch_coords = []

    latitude = None
    longitude = None

    for round in data:
        # If round is incorrect, we need to append the guessed lat and lng first
        # Afterwards, the actual attempt. Note that the target will be appended always
        # since if the guess was correct, the target is all we need
        # and otherwise, the guess comes before the target.

        if round['score'] == 0:
            latitude = round['guess']['lat']
            longitude = round['guess']['lng']

            batch_coords.append([latitude, longitude])
        
        latitude = round['target']['lat']
        longitude = round['target']['lng']

        batch_coords.append([latitude, longitude])

    return batch_coords

# Function for automating insertion into data table with two JSON files
def read_for_db_input_auto(json_file, json_api):
    with open(json_file) as json_data:
        file_data = json.load(json_data)

    round_length = len(file_data) # To be used for accessing the incorrect city guess

    # values that will be used to determine values that will be inputted into it

    for i in range(round_length):
        # Values that will be put into db_add
        guessed_city = None
        guessed_stc = None
        score = 1
        target_city = None
        target_stc = None
        guess_time = None

        if 'city' in json_api[i]:
            guessed_city = json_api[i]['city']

        # Might be changed later if it reaches the incorrect value
        target_city = guessed_city

        guessed_stc = abbreviation_decision(json_api[i])

        target_stc = guessed_stc
        
        if (file_data[i]['score'] == 0):
            score = 0

            target_city = json_api[round_length]['city']

            target_stc = abbreviation_decision(json_api[round_length])

        guess_time = file_data[i]['time']

        city_database.db_add(guessed_city, guessed_stc, score, target_city, target_stc, guess_time)

# Since only at most two JSON files will be added separately, manual will be a bit simpler
def read_for_db_input_manual(guessed_api, correct, target_api = None, time = None):
    # Getting JSON from the api calls
    guessed_json = guessed_api['results'][0]


    guessed_city = guessed_json['city']
    guessed_stc = abbreviation_decision(guessed_json)
    score = int(correct)
    target_city = None
    target_stc = None
    guess_time = time

    if target_api == None:
        target_city = guessed_city
        target_stc = guessed_stc
    else:
        target_json = target_api['results'][0]
        target_city = target_json['city']
        target_stc = abbreviation_decision(target_json)


    city_database.db_add(guessed_city, guessed_stc, score, target_city, target_stc, guess_time)

# Helper function for determining whether to abbreviate the state and country
def abbreviation_decision(json_info):
        
    # Criteria:
    # If the country has a valid state, it gets abbreviated
    # If the total length is greater than 25, the state also gets abbreviated

    # If the country lacks a state, and it's greater than 25 characters, it gets abbreviated.

    # Valid stated nations as API call often defines regions

    state = None
    state_code = None
    country = json_info['country']
    country_code = json_info['country_code']

    if ('state' in json_info):
            state = json_info['state']
            state_code = json_info['state_code']

    if (country_code == 'gb'):
        country_code = 'uk'
    
    # Valid nations with states based on own analysis; United States, Germany, Brazil, United Kingdom, India
    # Will add more based on user request
    valid_stated_nations = ['US','DE','UK','IN','BR']

    if state != None and country_code.upper() in valid_stated_nations:
        if len(state + ', ' + country_code) > 25:
            return state_code.upper() + ', ' + country_code.upper()
        return state + ', ' + country_code.upper()
    
    elif len(country) > 25:
        return country_code.upper()
    
    else:
        return country
        
    