import sys
import csv
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog,
                             QAction, QFrame, QGroupBox, QLineEdit, QFormLayout, QComboBox, QTableWidget, QTableWidgetItem, QDialog,
                             QRadioButton, QDateTimeEdit)
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor



class CoordinateSystemDialog(QDialog):
    def __init__(self, parent=None):
        super(CoordinateSystemDialog, self).__init__(parent)
        self.setWindowTitle("Coordinates")
        self.setGeometry(100, 100, 600, 400)

        self.coordinate_types_group = QGroupBox("Coordinate Types")
        self.cartesian_radio = QRadioButton("Cartesian (X, Y)")
        self.polar_radio = QRadioButton("Polar (θ, R)")
        self.cartesian_radio.setChecked(True)

        coordinate_types_layout = QVBoxLayout()
        coordinate_types_layout.addWidget(self.cartesian_radio)
        coordinate_types_layout.addWidget(self.polar_radio)
        self.coordinate_types_group.setLayout(coordinate_types_layout)

        self.x_scale_group = QGroupBox("X Coordinates")
        self.x_linear_radio = QRadioButton("Linear")
        self.x_log_radio = QRadioButton("Log")
        self.x_linear_radio.setChecked(True)
        self.x_units = QComboBox()
        self.x_units.addItems(["Number", "Time"])

        x_scale_layout = QVBoxLayout()
        x_scale_layout.addWidget(self.x_linear_radio)
        x_scale_layout.addWidget(self.x_log_radio)
        x_scale_layout.addWidget(QLabel("Units:"))
        x_scale_layout.addWidget(self.x_units)
        self.x_scale_group.setLayout(x_scale_layout)

        self.y_scale_group = QGroupBox("Y Coordinates")
        self.y_linear_radio = QRadioButton("Linear")
        self.y_log_radio = QRadioButton("Log")
        self.y_linear_radio.setChecked(True)
        self.y_units = QComboBox()
        self.y_units.addItems(["Number", "Time"])

        y_scale_layout = QVBoxLayout()
        y_scale_layout.addWidget(self.y_linear_radio)
        y_scale_layout.addWidget(self.y_log_radio)
        y_scale_layout.addWidget(QLabel("Units:"))
        y_scale_layout.addWidget(self.y_units)
        self.y_scale_group.setLayout(y_scale_layout)

        self.datetime_edit = QDateTimeEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.coordinate_types_group)
        layout.addWidget(self.x_scale_group)
        layout.addWidget(self.y_scale_group)
        layout.addWidget(QLabel("Date/Time:"))
        layout.addWidget(self.datetime_edit)
        layout.addStretch()

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class ImageViewer(QLabel):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.setMouseTracking(True)  # Ensure mouse tracking is enabled to receive mouse move events
        self.points = []
        self.lines = []
        self.current_line = []
        self.points_history = []
        self.redo_history = []
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setFixedSize(400, 300)
        self.setFrameShape(QFrame.Box)
        self.main_window = parent
        self.image_scale = (1, 1)
        self.select_mode = False
        self.selected_point = None

    def mouseMoveEvent(self, event):
        if self.select_mode and self.selected_point is not None:
            point, color = self.points[self.selected_point]
            self.points[self.selected_point] = ((event.x(), event.y()), color)
            self.update()
            self.main_window.update_points_table()
        else:
            super().mouseMoveEvent(event)
            if self.pixmap():
                self.show_magnified_area(event.pos())

    def show_magnified_area(self, position):
        size = 200  # Size of the magnification area
        magnification_factor = 2  # How much to magnify
        source_rect = QRect(position.x() - size // 2, position.y() - size // 2, size, size)
        if self.pixmap().rect().contains(source_rect):
            cropped = self.pixmap().copy(source_rect)
            scaled = cropped.scaled(size * magnification_factor, size * magnification_factor, Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
            self.main_window.canvas_label.setPixmap(scaled)

    def mousePressEvent(self, event):
        if self.select_mode:
            # Find the nearest point within a certain threshold
            min_dist = float('inf')
            for i, (point, color) in enumerate(self.points):
                dist = np.sqrt((point[0] - event.x()) ** 2 + (point[1] - event.y()) ** 2)
                if dist < min_dist and dist < 10:  # 10 pixels tolerance
                    min_dist = dist
                    self.selected_point = i
        else:
            if event.button() == Qt.LeftButton:
                x = event.pos().x() / self.image_scale[0]
                y = event.pos().y() / self.image_scale[1]
                color = self.main_window.color_selector.currentText().lower()
                self.points.append(((x, y), color))
                self.update()
                print(f"Point selected: ({x:.2f}, {y:.2f}) with color {color}")
                self.main_window.update_points_table()

                if self.main_window.draw_lines_button.isChecked():
                    self.current_line.append((x, y))
                    if len(self.current_line) == 2:
                        slope = self.main_window.calculate_slope(self.current_line[0], self.current_line[1])
                        self.lines.append((self.current_line, color, slope))
                        self.current_line = []
                        self.update()

    def mouseReleaseEvent(self, event):
        if self.select_mode and self.selected_point is not None:
            self.selected_point = None

    def paintEvent(self, event):

        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # For smoothing lines

        for point, color in self.points:
            painter.setPen(QPen(Qt.red if color == 'red' else
                                Qt.green if color == 'green' else
                                Qt.blue if color == 'blue' else
                                Qt.black, 5))
            x = point[0] * self.image_scale[0]
            y = point[1] * self.image_scale[1]
            painter.drawEllipse(QPoint(int(x), int(y)), 3, 3)

            # Drawing curves
        if len(self.points) > 1:
            path = QPainterPath()
            path.moveTo(self.points[0][0][0] * self.image_scale[0], self.points[0][0][1] * self.image_scale[1])
            for i in range(1, len(self.points)):
                x, y = self.points[i][0]
                mid_point_x = (self.points[i - 1][0][0] + x) / 2 * self.image_scale[0]
                mid_point_y = (self.points[i - 1][0][1] + y) / 2 * self.image_scale[1]
                path.quadTo(self.points[i - 1][0][0] * self.image_scale[0],
                                self.points[i - 1][0][1] * self.image_scale[1], mid_point_x, mid_point_y)

            color = self.points[-1][1]
            painter.setPen(QPen(QColor(color), 2))
            painter.drawPath(path)

    def undo_last_point(self):
        if self.points:
            self.redo_history.append(self.points.pop())
            self.update()
            self.main_window.update_points_table()

    def redo_last_point(self):
        if self.redo_history:
            self.points.append(self.redo_history.pop())
            self.update()
            self.main_window.update_points_table()

    def clear_points(self):
        self.points = []
        self.lines = []
        self.update()
        self.main_window.update_points_table()

    def clear_image(self):
        self.setPixmap(QPixmap())
        self.points = []
        self.lines = []
        self.update()
        self.main_window.update_points_table()

    def set_image(self, pixmap):
        self.setPixmap(pixmap)
        self.image_scale = (pixmap.width() / 400, pixmap.height() / 300)
        self.invert_colors()

    def invert_colors(self):
        if self.pixmap():
            image = self.pixmap().toImage()
            image.invertPixels(QImage.InvertRgb)
            self.setPixmap(QPixmap.fromImage(image))


    def draw_bezier_curves(self):
        self.update()  # updates for curves


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("NokDot")
        self.setGeometry(100, 100, 1200, 800)

        self.image_viewer = ImageViewer(self)  # Make sure to pass 'self' to access main_window in ImageViewer
        self.plot_viewer = QLabel()
        self.plot_viewer.setFixedSize(400, 300)
        self.plot_viewer.setFrameShape(QFrame.Box)



        self.load_image_button = QPushButton("Load Graph")
        self.load_image_button.clicked.connect(self.load_image)

        self.digitize_button = QPushButton("Digitize")
        self.digitize_button.clicked.connect(self.plot_scatter)

        self.draw_lines_button = QPushButton("Draw Lines")
        self.draw_lines_button.setCheckable(True)
        self.draw_lines_button.clicked.connect(self.toggle_draw_lines)


        self.points_table = QTableWidget()
        self.points_table.setColumnCount(3)  # X, Y, Slope sütunları
        self.points_table.setHorizontalHeaderLabels(["X", "Y", "Curve"])
        self.points_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.max_x_label = QLineEdit(self)
        self.max_y_label = QLineEdit(self)

        self.save_points_button = QPushButton("Save Points")
        self.save_points_button.clicked.connect(self.save_points)


        self.calculate_slope_button = QPushButton("Calculate Curve")
        self.calculate_slope_button.clicked.connect(self.calculate_slopes)


        self.color_selector = QComboBox(self)
        self.color_selector.addItems(["Red", "Green", "Blue", "Black"])

        self.create_top_menu()

        self.canvas_label = QLabel(self)  # Canvas for displaying images or graphics
        self.canvas_label.setFixedSize(200, 200)  # Square canvas
        self.canvas_label.setFrameShape(QFrame.Box)
        self.canvas_label.setStyleSheet("background-color: white;")  # White background for visibility

        image_group = QGroupBox("Graph")
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_viewer)
        image_group.setLayout(image_layout)


        plot_group = QGroupBox("Plot")
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot_viewer)
        plot_group.setLayout(plot_layout)

        form_layout = QFormLayout()
        form_layout.addRow("Max X Value:", self.max_x_label)
        form_layout.addRow("Max Y Value:", self.max_y_label)
        form_layout.addRow("Point Color:", self.color_selector)
        form_layout.addRow("Points List:", self.points_table)
        form_layout.addRow("", self.save_points_button)
        form_layout.addRow("", self.calculate_slope_button)
        form_layout.addRow("Canvas:", self.canvas_label)

        layout = QHBoxLayout()
        layout.addWidget(image_group)
        layout.addWidget(plot_group)
        layout.addLayout(form_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = None
        self.log_scale_x = False
        self.log_scale_y = False

    def create_top_menu(self):
        top_menu = self.menuBar()
        file_menu = top_menu.addMenu('File')
        edit_menu = top_menu.addMenu('Edit')
        digitize_menu = top_menu.addMenu('Digitize')
        view_menu = top_menu.addMenu('View')

        settings_menu = top_menu.addMenu('Settings')
        help_menu = top_menu.addMenu('Help')

        # Adding Import action
        import_action = QAction("Import...", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.import_data)  # Placeholder function
        file_menu.addAction(import_action)

        #Select Points Tool
        select_tool_action = QAction("Select Tool", self)
        select_tool_action.setCheckable(True)
        select_tool_action.triggered.connect(self.toggle_select_mode)
        digitize_menu.addAction(select_tool_action)

        #Digitize action
        digitize_action = QAction("Axis Point Tool", self)
        digitize_action.setShortcut("Ctrl+D")
        digitize_action.triggered.connect(self.plot_scatter)
        digitize_menu.addAction(digitize_action)

        #Draw lines action
        draw_lines_action = QAction("Point Match Tool", self)
        draw_lines_action.setShortcut("Ctrl+P")
        draw_lines_action.setCheckable(True)
        draw_lines_action.triggered.connect(self.toggle_draw_lines)
        digitize_menu.addAction(draw_lines_action)

        #Inverse Color tool
        color_picker_action = QAction("Color Picker Tool", self)
        color_picker_action.triggered.connect(self.image_viewer.invert_colors)
        digitize_menu.addAction(color_picker_action)

        # Adding Open action
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)  # Placeholder function
        file_menu.addAction(open_action)

        # Adding Save action
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)  # Placeholder function
        file_menu.addAction(save_action)

        # Adding Save As action
        save_as_action = QAction("Save As...", self)
        save_as_action.triggered.connect(self.save_file_as)  # Placeholder function
        file_menu.addAction(save_as_action)

        export_action = QAction("Export Data", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        # Adding Print action
        print_action = QAction("Print...", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_data)  # Placeholder function
        file_menu.addAction(print_action)

        # Adding Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)  # Uses the close method to exit
        file_menu.addAction(exit_action)


        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.image_viewer.undo_last_point)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.image_viewer.redo_last_point)
        edit_menu.addAction(redo_action)

        reset_action = QAction("Reset", self)  # Reset action
        reset_action.triggered.connect(self.reset_app)
        edit_menu.addAction(reset_action)

        coordinate_action = QAction("Coordinate System", self)
        coordinate_action.triggered.connect(self.open_coordinate_system_dialog)
        settings_menu.addAction(coordinate_action)

    def toggle_select_mode(self):
        if self.image_viewer.select_mode:
            self.image_viewer.select_mode = False
            self.image_viewer.selected_point = None
        else:
            self.image_viewer.select_mode = True

    def toggle_draw_lines(self):
        self.draw_lines_button.setChecked(not self.draw_lines_button.isChecked())

    def import_data(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                         "Image files (*.jpg *.jpeg *.png *.bmp)")
        if self.image_path:
            self.image_viewer.clear_points()
            pixmap = QPixmap(self.image_path)
            self.image_viewer.set_image(pixmap)
            self.plot_viewer.clear()  # Optional, clears the plot viewer if used elsewhere


    def open_file(self):
        print("Open file functionality not implemented.")

    def save_file(self):
        print("Save file functionality not implemented.")

    def save_file_as(self):
        print("Save file as functionality not implemented.")

    def print_data(self):
        print("Print functionality not implemented.")

    def load_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
        if self.image_path:
            self.image_viewer.clear_points()
            pixmap = QPixmap(self.image_path)
            self.image_viewer.set_image(pixmap)
            self.plot_viewer.clear()

    def save_points(self):
        if self.image_viewer.points:
            with open('selected_points.txt', 'w') as f:
                row_count = self.points_table.rowCount()
                for row in range(row_count):
                    x_value = self.points_table.item(row, 0).text()
                    y_value = self.points_table.item(row, 1).text()
                    slope_value = self.points_table.item(row, 2).text() if self.points_table.item(row, 2) else ""
                    f.write(f"{x_value},{y_value},{slope_value}\n")
                print("Points saved to selected_points.txt")
        else:
            print("No points selected.")

    def calculate_slopes(self):
        if len(self.image_viewer.points) < 2:
            print("Not enough points to calculate slopes.")
            return

        for i in range(len(self.image_viewer.points) - 1):
            point1 = self.image_viewer.points[i][0]
            point2 = self.image_viewer.points[i + 1][0]
            slope = self.calculate_slope(point1, point2)
            self.image_viewer.lines.append(([point1, point2], self.image_viewer.points[i][1], slope))

        self.update_points_table()
        print("Slopes calculated and updated.")

    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if path:
            try:
                if path.endswith('.csv'):
                    with open(path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['X', 'Y', 'Curve'])
                        for row in range(self.points_table.rowCount()):
                            x_value = self.points_table.item(row, 0).text()
                            y_value = self.points_table.item(row, 1).text()
                            slope_value = self.points_table.item(row, 2).text()
                            writer.writerow([x_value, y_value, slope_value])
                    print("Data exported to CSV successfully.")
                elif path.endswith('.xlsx'):
                    data = {
                        'X': [self.points_table.item(row, 0).text() for row in range(self.points_table.rowCount())],
                        'Y': [self.points_table.item(row, 1).text() for row in range(self.points_table.rowCount())],
                        'Curve': [self.points_table.item(row, 2).text() for row in range(self.points_table.rowCount())]
                    }
                    df = pd.DataFrame(data)
                    df.to_excel(path, index=False)
                    print("Data exported to Excel successfully.")
            except Exception as e:
                print("Failed to export data:", str(e))

    def update_points_table(self):
        try:
            max_x = float(self.max_x_label.text())
            max_y = float(self.max_y_label.text())
        except ValueError:
            max_x, max_y = 400, 300  # Default values if not set

        self.points_table.setRowCount(len(self.image_viewer.points))
        for i, (point, color) in enumerate(self.image_viewer.points):
            scaled_x = point[0] * self.image_viewer.image_scale[0] / 400 * max_x
            scaled_y = max_y - (point[1] * self.image_viewer.image_scale[1] / 300 * max_y)  # Inverted y-axis
            self.points_table.setItem(i, 0, QTableWidgetItem(f"{scaled_x:.1f}"))
            self.points_table.setItem(i, 1, QTableWidgetItem(f"{scaled_y:.1f}"))
            if i < len(self.image_viewer.lines):
                slope = self.image_viewer.lines[i][2]
                self.points_table.setItem(i, 2, QTableWidgetItem(f"{slope:.2f}"))

    def calculate_slope(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        if x2 != x1:
            return (y2 - y1) / (x2 - x1)
        else:
            return float('inf')

    def plot_scatter(self):
        points = np.array([point for point, color in self.image_viewer.points])
        if points.size == 0:
            return

        try:
            max_x = float(self.max_x_label.text())
            max_y = float(self.max_y_label.text())
        except ValueError:
            print("Invalid max X or Y value")
            return

        x = points[:, 0] * self.image_viewer.image_scale[0] / 400 * max_x
        y = max_y - (points[:, 1] * self.image_viewer.image_scale[1] / 300 * max_y)  # Inverted y-axis

        if self.log_scale_x:
            x = np.log10(x + 1)  # Apply log scale for X axis
        if self.log_scale_y:
            y = np.log10(y + 1)  # Apply log scale for Y axis

        colors = [color for point, color in self.image_viewer.points]

        plt.figure(figsize=(4, 3))
        for color in set(colors):
            mask = np.array(colors) == color
            plt.scatter(x[mask], y[mask], label=color, s=10, c=color)

            if self.draw_lines_button.isChecked():
                plt.plot(x[mask], y[mask], color=color, linestyle='-', marker='')

        plt.xlim([0, max_x if not self.log_scale_x else np.log10(max_x + 1)])
        plt.ylim([0, max_y if not self.log_scale_y else np.log10(max_y + 1)])
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.legend()
        plt.savefig("scatter.png", bbox_inches='tight')
        plt.close()
        scatter_image = Image.open("scatter.png")
        pixmap = QPixmap("scatter.png")
        self.plot_viewer.setPixmap(pixmap)
        self.image_viewer.draw_bezier_curves()

    def reset_app(self):
        self.image_viewer.clear_image()
        self.plot_viewer.clear()
        self.max_x_label.clear()
        self.max_y_label.clear()
        self.points_table.setRowCount(0)
        self.log_scale_x = False
        self.log_scale_y = False
        self.draw_lines_button.setChecked(False)

    def open_coordinate_system_dialog(self):
        dialog = CoordinateSystemDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Coordinate settings updated")
            self.log_scale_x = dialog.x_log_radio.isChecked()
            self.log_scale_y = dialog.y_log_radio.isChecked()
            self.plot_scatter()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())