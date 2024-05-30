from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotWindow(QDialog):
    def __init__(self, data_points, interpolated_points=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data Points Plot")
        self.setGeometry(100, 100, 800, 600)

        self.data_points = data_points
        self.interpolated_points = interpolated_points

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Matplotlib canvas
        self.canvas = FigureCanvas(Figure())
        layout.addWidget(self.canvas)

        # Plot options
        options_layout = QHBoxLayout()

        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)
        options_layout.addWidget(self.plot_button)

        self.graph_type_label = QLabel("Graph Type:")
        options_layout.addWidget(self.graph_type_label)

        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Scatter", "Line", "Bar"])
        options_layout.addWidget(self.graph_type_combo)

        self.filter_label = QLabel("Filter Y >")
        options_layout.addWidget(self.filter_label)

        self.filter_input = QLineEdit()
        options_layout.addWidget(self.filter_input)

        self.apply_filter_button = QPushButton("Apply Filter")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        options_layout.addWidget(self.apply_filter_button)

        layout.addLayout(options_layout)

        self.setLayout(layout)

    def plot_data(self):
        ax = self.canvas.figure.subplots()
        ax.clear()

        valid_data_points = [point for point in self.data_points if point.get_real_coordinates() is not None]
        x_coords = [point.get_real_coordinates().x() for point in valid_data_points]
        y_coords = [point.get_real_coordinates().y() for point in valid_data_points]

        graph_type = self.graph_type_combo.currentText()
        if graph_type == "Scatter":
            ax.scatter(x_coords, y_coords, c='blue', label='Data Points')
        elif graph_type == "Line":
            ax.plot(x_coords, y_coords, c='blue', label='Data Points')
        elif graph_type == "Bar":
            ax.bar(x_coords, y_coords, color='blue', label='Data Points')

        if self.interpolated_points:
            valid_interpolated_points = [point for point in self.interpolated_points if
                                         point.get_real_coordinates() is not None]
            x_interp_coords = [point.get_real_coordinates().x() for point in valid_interpolated_points]
            y_interp_coords = [point.get_real_coordinates().y() for point in valid_interpolated_points]
            if graph_type == "Scatter":
                ax.scatter(x_interp_coords, y_interp_coords, c='red', label='Interpolated Points')
            elif graph_type == "Line":
                ax.plot(x_interp_coords, y_interp_coords, c='red', label='Interpolated Points')
            elif graph_type == "Bar":
                ax.bar(x_interp_coords, y_interp_coords, color='red', label='Interpolated Points')

        ax.set_xlabel('X Coordinates')
        ax.set_ylabel('Y Coordinates')
        ax.set_title('Data Points Plot')
        ax.legend()
        self.canvas.draw()

    def apply_filter(self):
        filter_value = self.filter_input.text()
        try:
            filter_value = float(filter_value)
        except ValueError:
            return  # Invalid input, ignore

        filtered_data_points = [point for point in self.data_points if point.get_real_coordinates().y() > filter_value]
        self.data_points = filtered_data_points
        self.plot_data()
