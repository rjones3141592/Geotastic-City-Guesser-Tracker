import sqlite3
connection = None

STAT_FILE = "GT_stat_file.db"

# Counts number of correct and incorrect values to put into Numpy
def count_correct_incorrect():
    connection = sqlite3.connect(STAT_FILE)
    cursor = connection.cursor()

    try:
        output = cursor.execute("SELECT correct_guess, COUNT(*) as num_correct FROM city_stats GROUP BY correct_guess").fetchall()
        
        incorrect_tuple = output[0]
        correct_tuple = output[1]

        incorrect_count = incorrect_tuple[1]
        correct_count = correct_tuple[1]

        return [correct_count, incorrect_count]

    except sqlite3.OperationalError as error_code:
        print("Failed to read database! Error Code: ", error_code)

    finally:
        connection.close()