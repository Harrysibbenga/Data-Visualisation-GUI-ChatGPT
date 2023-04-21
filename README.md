# Temperature Graph App
This is a simple GUI application for generating a line graph of temperature data from a CSV file. The application is built using Python 3 and PyQt5.

## Requirements
To run the application, you will need:

Python 3.x
PyQt5
pandas
matplotlib
Installation
To install the required packages, you can use pip:

Copy code
```
pip install pyqt5 pandas matplotlib
```
Usage
To run the application, simply run the main.py file:


Copy code
```
python main.py
```
The application will open a window with the following options:

A label showing the currently selected CSV file.
A button to select a CSV file.
A date range selector to select the start and end dates for the data to be plotted.
A button to generate the graph.
A graph area displaying the generated line graph.
To generate a graph, follow these steps:

Click the "Select CSV File" button and choose a CSV file with temperature data. The selected file will be displayed in the label.
Choose a start and end date for the data to be plotted using the date range selector.
Click the "Generate Graph" button to plot the data.
The line graph will be displayed in the graph area.

License
This project is licensed under the MIT License. See the LICENSE file for details.