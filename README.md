# Geotastic-City-Guesser-Tracker

This is a program that aims to track city guesses on highscore hunts on Geotastic for small data analyzing purposes. If you wish to see what cities you consistently guess right, which ones you don't, among other statistics such as timing and streak averages, this is the program for you!

## IMPORTANT INFORMATION
This program relies on Geoapify for reverse GIS lookups, and an API key is required for free functionality. When contacting them, they recommended each user create an account that allows them to have their own API key for usage. An account can be made here:

https://www.geoapify.com/

When you obtain your API key, you can insert it into the API Key field in the Settings tab.

## Program Features
### Data Importing
<img width="945" height="394" alt="image" src="https://github.com/user-attachments/assets/15b88b78-2669-4e08-8454-1525bafd02fb" />

Data can be imported on the first tab of the program. There are two methods by which you can import data onto your local database:
- Manual Insertion: Typing in all fields necessary and hitting "Insert Guess"
- File Importing: Geotastic provides JSON files that you can download; hitting "Import JSON File" will enable you to select JSON files for it to comb through; note that you can multi-select JSON files.

### Guess History
<img width="942" height="366" alt="image" src="https://github.com/user-attachments/assets/567adbc9-21fa-4ee0-9513-e05f2dc85503" />

This tab allows you to see all cities guessed (that you have imported onto the program). This will also allow you to delete any data entries via highlighting them and clicking "delete selected". In addition, you can also edit an entry via double clicking a row.

### Statistics
This tab provides you with numerical/quantitative analysis of your imported data. There are four tabs included: Overview, Time, Accuracy & Streaks, and Cities.

#### Overview
<img width="942" height="346" alt="image" src="https://github.com/user-attachments/assets/c2b8f50c-b5c4-4882-a175-63640702d957" />

Overview provides a surface level look into your performance, with your overall average guessing percentage, the average time it takes for you to guess, your record longest streak, and your most played country.

#### Time
<img width="945" height="342" alt="image" src="https://github.com/user-attachments/assets/94187f05-e8da-4f5c-a822-2a75f931de7f" />

Time shows analysis regarding your timing when guessing. It shows you your average guess time, as well as showing the average among correct and incorrect guess times as well. It also provides your fastest recorded guesses for both correct and incorrect results.

#### Accuracy & Streaks
<img width="945" height="401" alt="image" src="https://github.com/user-attachments/assets/db5d10d9-ab96-408b-ab6d-7fff859e7f00" />

This tab provides details regarding your streak history (as this is a program made for the highscore hunt gamemode). It shows your overall accuracy, your average streak length, and longest streak. This tab also can show you two charts: one for your recent round line chart (defaulting to the last 10 rounds, though you can change this in settings) or a histogram of all rounds imported.

#### Cities
<img width="942" height="356" alt="image" src="https://github.com/user-attachments/assets/4520f29b-a785-47b0-91f1-2f3503f768a8" />

The cities tab provides you with two top-5 lists, one for the cities you've guessed correctly most often (prioritizing 'correct guesses total' rather than percent out of total times you guessed a city), and one for the cities you've guessed incorrectly most often (with priority going for most incorrect guesses before percent correctly guessed).

### Settings
<img width="944" height="400" alt="image" src="https://github.com/user-attachments/assets/8b5a6076-4478-4388-b031-fff59f64dd46" />

The Settings tab provides you with some ways for you to customize the program: a dark mode, ability to confirm exit & confirm deleting items in your database, and modifying the number of rounds shown in the Accuracy & streaks line chart.

This tab also is where you would import your Geoapify API key.

## Status

This project is currently in version 1.0.0! 

For MacOS users, you might get a "cannot be opened because it is from an unidentified developer". You can circumvent this via right-click/control clicking and hitting "open" and then "open" again.

### Updates:

7/23/2025 - Holy crap I got in contact with Edutastic (dev of Geotastic), there might be a major revamp of this project with the possibility of importing exported completed highscore hunts!

7/27/2025 - I got sql visualization working! You can now see the guessing history from the Guess History Tab!

7/29/2025 - Importing of JSON files downloadable after rounds now work! I need to modify the manual insertion to also rely on API calls.

7/31/2025 - Both manual and JSON data insertions now use API calls to standardize data inputs in the SQL database!

8/11/2025 - Overall Stat Overview now added! Will be adding more advanced/deeper statistics down the line.

8/24/2025 - Back in University so progress will be slowed; Timing tab + Accuracy * Streaks tab are both online!

8/31/2025 - Allows for editing of database city names through history table & double clicking on an entry in the history table! Note that it will only allow for changing both guessed and target cities if the round was incorrect.

5/2/2026 - Importing Files now allows users to select multiple JSON files at once! It will cycle through all files and insert them into the database.

8/17/2026 - Version v1.0.0 is now live! 

## Special Thanks

To James for convincing to contact Edutastic and asking about getting a better way to input data, only for him to go and add a feature specifically for me (and also "for own leisure"); holy cow I did NOT expect that.
