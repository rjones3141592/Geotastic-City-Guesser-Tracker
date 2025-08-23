from matplotlib.figure import Figure
import numpy as np
import stat_queries

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

def rolling_average_line(data):
    line_plot_labels = ['Recent AVG','Overall AVG']
    # Recent Average, Overall Average

    fig = Figure(figsize = (4,3))
    fig.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))
    fig.subplots_adjust(left = 0.15, right = .95, top = .9, bottom = 0.15)
    rolling_line_plot = fig.add_subplot(111)
    rolling_line_plot.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))
    # Rolling averages
    rolling_line_plot.plot(data, color = "#6699DB")

    rolling_line_plot.axhline(stat_queries.percent_accuracy(), color = "#E5AC6B")

    rolling_line_plot.legend(loc = 'upper right', labels = line_plot_labels)
    rolling_line_plot.set_title('Rolling Accuracy')
    rolling_line_plot.set_xlabel('Round #')
    rolling_line_plot.set_ylabel('Accuracy (%)')
    
    rolling_line_plot.set_ybound(0, 100)
    rolling_line_plot.set_yticks(range(0, 101, 10))
    rolling_line_plot.set_xlim(1, len(data))

    fig.tight_layout()
    
    return rolling_line_plot, fig