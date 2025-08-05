import sqlite3
import city_database
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
        
        return str(accuracy) + '%'

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
        output = cursor.execute("SELECT AVG(guess_time) FROM city_stats").fetchall()
        
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
def most_played_countries():
    pass