import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QPushButton, QFileDialog, QDateEdit, QWidget, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Temperature Graph")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 800, 600)

        # create the UI elements here
        # create a label to display the selected file name
        self.filename_label = QLabel("No file selected.")
        self.filename_label.setAlignment(Qt.AlignCenter)

        # create a button to select the csv file
        self.select_file_button = QPushButton("Select CSV File")
        self.select_file_button.clicked.connect(self.select_file)

        # create a date range selector
        self.start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)

        self.end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)

        # create a combo box for selecting the graph type
        self.graph_type_label = QLabel("Graph Type:")
        self.graph_type_combo_box = QComboBox()
        self.graph_type_combo_box.addItem("Line Graph")
        self.graph_type_combo_box.addItem("Bar Graph")

        # create a button to generate the graph
        self.generate_graph_button = QPushButton("Generate Graph")
        self.generate_graph_button.clicked.connect(self.generate_graph)

        # create a matplotlib figure and canvas
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)

        # create a layout for the top section of the GUI
        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.filename_label)
        self.top_layout.addWidget(self.select_file_button)
        self.top_layout.addWidget(self.start_date_label)
        self.top_layout.addWidget(self.start_date_edit)
        self.top_layout.addWidget(self.end_date_label)
        self.top_layout.addWidget(self.end_date_edit)
        self.top_layout.addWidget(self.graph_type_label)
        self.top_layout.addWidget(self.graph_type_combo_box)
        self.top_layout.addWidget(self.generate_graph_button)

        # create a layout for the entire GUI and add the top and canvas layouts to it
        self.layout = QGridLayout()
        self.layout.addLayout(self.top_layout, 0, 0)
        self.layout.addWidget(self.canvas, 1, 0)

        # create a central widget and set the layout
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        if filename:
            self.filename_label.setText(filename)

    def generate_graph(self):
        filename = self.filename_label.text()
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        data = pd.read_csv(filename)
        data[ "Date" ] = pd.to_datetime(data[ "Date" ])
        data = data[ (data[ "Date" ]>=start_date) & (data[ "Date" ]<=end_date) ]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Add user choice for type of graph
        graph_type = self.graph_type_combo_box.currentText()
        if graph_type=="Line Graph":
            ax.plot(data[ "Date" ], data[ "Temperature" ])
        elif graph_type=="Bar Graph":
            ax.bar(data[ "Date" ], data[ "Temperature" ])

        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # set the initial focus to the select file button
    window.select_file_button.setFocus()

    sys.exit(app.exec_())
