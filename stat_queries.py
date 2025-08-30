import sqlite3
import city_database
from iso3166 import countries
connection = None

STAT_FILE = "GT_stat_file.db"

# Counts number of correct and incorrect values to put into Numpy
def count_correct_incorrect():
    # Empty_case check
    if city_database.db_is_empty():
        return [0, 0]

    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    try:
        output = cursor.execute("SELECT correct_guess, COUNT(*) as num_correct FROM city_stats GROUP BY correct_guess").fetchall()

        correct_count = 0
        incorrect_count = 0

        for guess, count in output:
            if guess == 1: # correct guess
                correct_count = count
            else: # incorrect
                incorrect_count = count

        return [correct_count, incorrect_count]

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# Gets accuracy in percentage format (xx.xx%)
def percent_accuracy():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    if city_database.db_is_empty():
        return 'N/A'

    try:
        output = cursor.execute("SELECT correct_guess, COUNT(*) as num_correct FROM city_stats GROUP BY correct_guess").fetchall()

        correct_count = 0
        total_count = 0

        for guess, count in output:
            if guess == 1: # correct guess
                correct_count = count
                total_count += count
            else:
                total_count += count


        if total_count == 0:
            total_count += 1

        accuracy = round((correct_count / float(total_count)) * 100, 2)
        
        return str(accuracy)

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# Deduces the average time to guess per round
def average_time():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    # Empty_case check
    if city_database.db_is_empty():
        return 'N/A'

    try:
        output = cursor.execute("SELECT AVG(guess_time) FROM city_stats WHERE guess_time IS NOT NULL").fetchall()
        
        avg_time = round(output[0][0], 2)
        
        return str(avg_time) + ' seconds'

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# finds longest streak of correct guesses
def longest_streak():
    # Empty_case check
    if city_database.db_is_empty():
        return 'N/A'

    longest_streak = 0

    current_streak = 0

    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        read_all = cursor.execute('SELECT id, correct_guess FROM city_stats ORDER BY id DESC')
        data = read_all.fetchall()

        # Goes through each entry, finding sequences of '1' answers.
        for entry in data:
            if entry[1] == 1:
                current_streak += 1
            else:
                if (current_streak > longest_streak):
                    longest_streak = current_streak

                current_streak = 0
        
        if current_streak > longest_streak:
            longest_streak = current_streak

        return longest_streak
                
    
    except sqlite3.OperationalError as error_code:
        print('Failed to read data!', error_code)
        return None

    finally:
        connection.close()

# Uses Dictionary to extract most played country
def most_played_country():
    # Empty_case check
    if city_database.db_is_empty():
        return 'N/A'

    countries_played = {}

    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        read_all = cursor.execute('SELECT correct_state_country FROM city_stats ORDER BY id DESC')
        data = read_all.fetchall()

        # Goes through each entry, finding sequences of '1' answers.
        for entry in data:
            if ',' in entry[0]:
                entry_list = entry[0].split(',')
                country_name = entry_list[1].strip()
            else:
                country_name = entry[0]

            if country_name in countries_played:
                countries_played[country_name] += 1
            else:
                countries_played[country_name] = 1

        most_played = max(countries_played, key = lambda x: countries_played[x])

        most_country_name = countries.get(most_played).name
        
        return most_country_name
                
    
    except sqlite3.OperationalError as error_code:
        print('Failed to read data!', error_code)
        return None

    finally:
        connection.close()

# Gets times for correct and incorrect guesses and returns them for histogram
def times_for_correct_incorrect():
    # Empty_case check
    if city_database.db_is_empty():
        return [[],[]]

    correct_times = []
    incorrect_times = []

    connection = sqlite3.connect("GT_stat_file.db")
    cursor = connection.cursor()
    try:
        # Reads database for both correct_guess = 1 and correct_guess = 0 and extends their respective lists
        read_all = cursor.execute('SELECT guess_time FROM city_stats WHERE correct_guess = 1 AND guess_time IS NOT NULL')
        data = read_all.fetchall()

        correct_times.extend(time[0] for time in data)

        read_all = cursor.execute('SELECT guess_time FROM city_stats WHERE correct_guess = 0 AND guess_time IS NOT NULL')
        data = read_all.fetchall()

        incorrect_times.extend(time[0] for time in data)

        return [correct_times, incorrect_times]
    
    except sqlite3.OperationalError as error_code:
        print('Failed to read data!', error_code)
        return None

    finally:
        connection.close()

# Deduces the average time to guess per round between correct guesses & incorrect guesses
def average_times_correct_incorrect():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    # Empty_case check
    if city_database.db_is_empty():
        return ['N/A','N/A']

    try:
        # Executes two AVG calls onto the database
        output = cursor.execute("SELECT AVG(guess_time) FROM city_stats WHERE correct_guess = 1 AND guess_time IS NOT NULL").fetchall()
        avg_correct_time = round(output[0][0], 2)

        output = cursor.execute("SELECT AVG(guess_time) FROM city_stats WHERE correct_guess = 0 AND guess_time IS NOT NULL").fetchall()
        avg_incorrect_time = round(output[0][0], 2)
        
        # Gives both in one line, and can be accessed through list indexing
        return [str(avg_correct_time) + ' seconds', str(avg_incorrect_time) + ' seconds']

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# Gets the fastest and slowest time where a correct guess was made
def fastest_slowest_correct_time():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    # Empty_case check
    if city_database.db_is_empty():
        return ['N/A','N/A']

    try:
        # Finds slowest correct time
        output = cursor.execute("SELECT correct_city, correct_state_country, guess_time FROM city_stats WHERE correct_guess = 1 AND guess_time IS NOT NULL ORDER BY guess_time DESC LIMIT 1").fetchall()
        slowest_time = f'{output[0][0]}, {output[0][1]} ({output[0][2]} seconds)'

        # Finds fastest correct time
        output = cursor.execute("SELECT correct_city, correct_state_country, guess_time FROM city_stats WHERE correct_guess = 1 AND guess_time IS NOT NULL ORDER BY guess_time LIMIT 1").fetchall()
        fastest_time = f'{output[0][0]}, {output[0][1]} ({output[0][2]} seconds)'

        return [fastest_time, slowest_time]

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# Obtains streaks and puts it in a list for histogram.
def all_streaks():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    # Empty_case check
    if city_database.db_is_empty():
        return ['N/A']

    try:
        streak = 0
        streaks_list = []
        # Finds slowest correct time
        data = cursor.execute("SELECT correct_guess FROM city_stats").fetchall()
        for guess in data:
            # Correct Guess
            if guess[0] == 1:
                streak += 1
            else:
                streaks_list.append(streak)
                streak = 0
        if streak != 0:
            streaks_list.append(streak)

        return streaks_list

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()

# Gets accuracy of each round, with a setting to change amount of rounds shown in database
def rolling_round_accuracy():
    # Gets accuracy of each round by adding one and then dividing
    data = all_streaks()

    round_accuracy = []

    for entry in data:
        pc_accuracy = round((entry / float(entry + 1)) * 100, 2)
        round_accuracy.append(pc_accuracy)
        
    return round_accuracy[-10:]

# Gets average streak
def average_streaks():
    data = all_streaks()

    data_sum = sum(data)

    average = data_sum / len(data)

    return round(average, 2)

# Gets top 5 round
def most_correct_cities():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    # Empty_case check
    if city_database.db_is_empty():
        return 'N/A'

    try:
        output = cursor.execute("SELECT AVG(correct_guess), SUM(correct_guess), COUNT(*), correct_city, correct_state_country FROM city_stats GROUP BY correct_city, correct_state_country ORDER BY SUM(correct_guess) DESC, AVG(correct_guess) DESC, COUNT(*) DESC").fetchall()
        print(output)

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()