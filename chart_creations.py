from matplotlib.figure import Figure
import numpy as np

def percent_correct_pie(data):
    right_wrong_labels = ['Correct','Incorrect']

    fig = Figure(figsize = (3, 3))

    fig.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))

    fig.subplots_adjust(left = 0, right = 1, top = 1, bottom = 0)

    accuracy_figure = fig.add_subplot(111)

    accuracy_figure.patch.set_facecolor((240 / 255.0, 240 / 255.0 , 240 / 255.0, 1))

    accuracy_figure.pie(data, radius = 1, labels = ['',''], autopct = '%0.2f%%', shadow = False, colors = ['#8AEA95', '#E5716B'])

    accuracy_figure.legend(loc = 'upper right', labels = right_wrong_labels)
    
    return accuracy_figure, fig