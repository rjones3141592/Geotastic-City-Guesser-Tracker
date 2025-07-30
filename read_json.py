import json
import city_database

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

def read_for_db_input_auto(json_file, json_api):
    with open(json_file) as json_data:
        file_data = json.load(json_data)

    round_length = len(file_data) # To be used for accessing the incorrect city guess

    # Values that will be put into db_add
    guessed_city = None
    guessed_stc = None
    score = 1
    target_city = None
    target_stc = None
    guess_time = None

    # values that will be used to determine values that will be inputted into it
    state_name = None
    state_code = None

    print(round_length)

    for i in range(round_length):

        guessed_city = json_api[i]['city']
        # Might be changed later if it reaches the incorrect value
        target_city = guessed_city

        if ('state' in json_api[i]):
            state_name = json_api[i]['state']
            state_code = json_api[i]['state_code']
        
        
        guessed_stc = abbreviation_decision(json_api[i]['country'], json_api[i]['country_code'], state_name, state_code)

        target_stc = guessed_stc

        
        if (file_data[i]['score'] == 0):
            score = 0

            target_city = json_api[round_length]['city']

            if ('state' in json_api[i]):
                state_name = json_api[round_length]['state']
                state_code = json_api[round_length]['state_code']
            else:
                state_name = None
                state_code = None
            
            target_stc = abbreviation_decision(json_api[i]['country'], json_api[i]['country_code'], state_name, state_code)

        guess_time = file_data[i]['time']

        city_database.db_add(guessed_city, guessed_stc, score, target_city, target_stc, guess_time)




# Helper function for determining whether to abbreviate the state and country
def abbreviation_decision(country, country_code, state = None, state_code = None):
        
    # Criteria:
    # If the country has a valid state, it gets abbreviated
    # If the total length is greater than 25, the state also gets abbreviated

    # If the country lacks a state, and it's greater than 25 characters, it gets abbreviated.

    # Valid stated nations as API call often defines regions
    valid_stated_nations = ['US','DE','UK','IN']


    if state != None and country_code.upper() in valid_stated_nations:
        if len(state + ', ' + country_code) > 25:
            return state_code.upper() + ', ' + country_code.upper()
        return state + ', ' + country_code.upper()
    
    elif len(country) > 25:
        return country_code.upper()
    
    else:
        return country
        
    