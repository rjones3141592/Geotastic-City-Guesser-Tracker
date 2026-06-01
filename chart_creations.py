from matplotlib.figure import Figure
import numpy as np
import stat_queries
from matplotlib.ticker import MaxNLocator


def percent_correct_pie(data):
    right_wrong_labels = ['Correct','Incorrect']

    # Configuring figure visuals
    fig = Figure(figsize = (3, 3))
    fig.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    fig.subplots_adjust(left = 0, right = 1, top = 1, bottom = 0)
    accuracy_figure = fig.add_subplot(111)
    accuracy_figure.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))

    # Creating pie chart with legend
    accuracy_figure.pie(data, radius = 1, labels = ['',''], autopct = '%0.2f%%', shadow = False, colors = ['#8AEA95', '#E5716B'])

    accuracy_figure.legend(loc = 'upper right', labels = right_wrong_labels)
    
    # Returning to allow for refreshing within overall_tab
    return accuracy_figure, fig

# Creates stacked histogram of correct and incorrect timings
def time_histogram(data):
    histogram_labels = ['Correct Times', 'Incorrect Times']

    # Configuring figure visuals
    fig = Figure(figsize = (4,3))
    fig.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    fig.subplots_adjust(left = 0.15, right = .95, top = .9, bottom = 0.15)
    timing_histogram = fig.add_subplot(111)
    timing_histogram.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    timing_histogram.hist(data, bins = 30, stacked = True, rwidth = 0.9, color = ['#8AEA95', '#E5716B'])

    timing_histogram.legend(loc = 'best', labels = histogram_labels)
    timing_histogram.set_title('Timing Distribution')
    timing_histogram.set_xlabel('Time (s)')
    timing_histogram.set_ylabel('Frequency')

    timing_histogram.yaxis.set_major_locator(MaxNLocator(integer = True))

    fig.tight_layout()

    return timing_histogram, fig

def rolling_average_line(data):
    line_plot_labels = ['Recent AVG','Overall AVG']
    # Recent Average, Overall Average

    fig = Figure(figsize = (4,3))
    fig.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    fig.subplots_adjust(left = 0.15, right = .95, top = .9, bottom = 0.15)
    rolling_line_plot = fig.add_subplot(111)
    rolling_line_plot.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    # Rolling averages
    rolling_line_plot.plot(data, color = "#6699DB")

    # Overall average as an axis oline
    rolling_line_plot.axhline(float(stat_queries.percent_accuracy()), color = "#E5AC6B", ls = '--')
    
    # Setting labels and legend
    rolling_line_plot.legend(loc = 'best', labels = line_plot_labels)
    rolling_line_plot.set_title('Rolling Accuracy - Past 10 Rounds')
    rolling_line_plot.set_xlabel('Recent Round #')
    rolling_line_plot.set_ylabel('Accuracy (%)')
    
    # Setting boundaries of chart with reverse x tick label
    rolling_line_plot.set_ylim(0, 100)
    rolling_line_plot.set_yticks(range(0, 101, 10))
    rolling_line_plot.set_xlim(0, len(data)-1)
    rolling_line_plot.set_xticks(range(0, 10))
    rolling_line_plot.set_xticklabels([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    fig.tight_layout()
    
    return rolling_line_plot, fig

def streaks_histogram(data):
    # Configuring figure visuals
    fig = Figure(figsize = (4,3))
    fig.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))
    fig.subplots_adjust(left = 0.15, right = .95, top = .9, bottom = 0.15)
    streak_histogram = fig.add_subplot(111)
    streak_histogram.patch.set_facecolor((220 / 255.0, 218 / 255.0 , 213 / 255.0, 1))

    # Setting bins to be from 0 to max(data) + 2 to ensure even spacing (and integer evaluations of streak distribution)
    streak_histogram.hist(data, bins = range(0, max(data) + 2), align = 'left', rwidth = 0.9, color = '#6699DB')

    streak_histogram.set_title('Streaks Distribution')
    streak_histogram.set_xlabel('Streak Amount')
    streak_histogram.set_ylabel('Frequency')

    streak_histogram.xaxis.set_major_locator(MaxNLocator(integer = True))
    streak_histogram.yaxis.set_major_locator(MaxNLocator(integer = True))

    fig.tight_layout()

    return streak_histogram, fig