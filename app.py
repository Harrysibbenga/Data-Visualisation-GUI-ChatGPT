import csv
from datetime import datetime
from bokeh.io import show
from bokeh.models import ColumnDataSource, DateRangeSlider
from bokeh.models.widgets import Button
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.events import ButtonClick
from bokeh.models import CustomJS

from tkinter import *
from tkinter import ttk

# Read the data from the CSV file
with open('temperature_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    date_data, temperature_data = [ ], [ ]
    for row in reader:
        try:
            date_data.append(datetime.strptime(row[ 0 ], '%Y-%m-%d'))
            temperature_data.append(float(row[ 1 ]))
        except ValueError:
            continue

# Create a ColumnDataSource object with the data
source = ColumnDataSource(data = dict(date = date_data, temperature = temperature_data))

# Create a figure object for the graph
p = figure(title = 'Temperature Data', x_axis_type = 'datetime', width = 800, height = 400)
p.line(x = 'Date', y = 'Temperature', source = source)

# Create a DateRangeSlider for selecting the date range
start_date = min(date_data)
end_date = max(date_data)
date_range_slider = DateRangeSlider(title = 'Date Range', start = start_date, end = end_date,
                                    value = (start_date, end_date))


# Create a button for generating the graph
def update_graph():
    # Get the selected date range from the DateRangeSlider
    start, end = date_range_slider.value_as_datetime

    # Filter the data to include only the selected dates
    filtered_data = dict(date = [ ], temperature = [ ])
    for i in range(len(date_data)):
        if start<=date_data[ i ]<=end:
            filtered_data[ 'Date' ].append(date_data[ i ])
            filtered_data[ 'Temperature' ].append(temperature_data[ i ])

    # Update the ColumnDataSource with the filtered data
    source.data = filtered_data


# Create a button for generating the graph
button = Button(text = 'Generate Graph')
# button.on_event(update_graph)

# Create a CustomJS callback to update the plot
callback = CustomJS(args = dict(source = source), code = """
    // Get the selected date range from the DateRangeSlider
    var start = new Date(document.querySelector('#date_range_slider').value[0])
    var end = new Date(document.querySelector('#date_range_slider').value[1])

    // Filter the data to include only the selected dates
    var filtered_data = { date: [], temperature: [] }
    for (var i = 0; i < source.data.date.length; i++) {
        var date = new Date(source.data.date[i])
        if (start <= date && date <= end) {
            filtered_data.date.push(source.data.date[i])
            filtered_data.temperature.push(source.data.temperature[i])
        }
    }

    // Update the ColumnDataSource with the filtered data
    source.data = filtered_data
    source.change.emit()
""")

# Attach the callback to the button
button.on_event(ButtonClick, update_graph)
# Create a Tkinter window
root = Tk()
root.title("Temperature Data Visualization")

# Create a frame to hold the Bokeh plot and controls
frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10, sticky=(N, S, E, W))

# Add the plot and controls to the frame
p_widget = show(p, include_plotlyjs = False, output_type = "div", CDN = CDN)
plot_frame = ttk.Frame(frame)
plot_frame.grid(column = 0, row = 0, padx = 10, pady = 10, sticky = (N, S, E, W))
plot_frame.columnconfigure(0, weight = 1)
plot_frame.rowconfigure(0, weight = 1)
plot_widget = ttk.Label(plot_frame, text = p_widget, justify = "center")
plot_widget.grid(column = 0, row = 0, sticky = (N, S, E, W))
control_frame = ttk.Frame(frame)
control_frame.grid(column = 0, row = 1, padx = 10, pady = 10, sticky = (E, W))
date_range_slider_widget = show(date_range_slider, include_plotlyjs = False, output_type = "div", CDN = CDN)
slider_widget = ttk.Label(control_frame, text = date_range_slider_widget, justify = "center")
slider_widget.grid(column = 0, row = 0, sticky = (N, S, E, W))
button_widget = ttk.Button(control_frame, text = "Generate Graph", command = update_graph)
button_widget.grid(column = 1, row = 0, padx = 10, sticky = (N, S, E, W))

root.mainloop()
