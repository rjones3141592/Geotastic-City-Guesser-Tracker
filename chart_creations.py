from matplotlib.figure import Figure
import numpy as np

def percent_correct_pie(data):
    right_wrong_labels = ['Correct','Incorrect']

    # Configuring figure visuals
    fig = Figure(figsize = (3, 3))
    fig.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))
    fig.subplots_adjust(left = 0, right = 1, top = 1, bottom = 0)
    accuracy_figure = fig.add_subplot(111)
    accuracy_figure.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))

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
    fig.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))
    fig.subplots_adjust(left = 0.15, right = .95, top = .9, bottom = 0.15)
    timing_histogram = fig.add_subplot(111)
    timing_histogram.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))
    timing_histogram.hist(data, bins = 30, stacked = True, color = ['#8AEA95', '#E5716B'])

    timing_histogram.legend(loc = 'upper right', labels = histogram_labels)
    timing_histogram.set_title('Timing Distribution')
    timing_histogram.set_xlabel('Time (s)')
    timing_histogram.set_ylabel('Frequency')

    fig.tight_layout()

    return timing_histogram, fig