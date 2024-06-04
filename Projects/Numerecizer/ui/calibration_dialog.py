from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class CalibrationDialog(QDialog):
    """Dialog to input real coordinates for calibration points."""

    def __init__(self, parent=None, automatic_calibration=False):
        super().__init__(parent)
        self.real_coordinates = None
        self.automatic_calibration = automatic_calibration
        self.initUI()

    def initUI(self):
        """Initializes the UI components."""
        self.setWindowTitle("Enter Real Coordinates")

        layout = QVBoxLayout()

        self.x_label = QLabel("X Coordinate:")
        self.x_input = QLineEdit()
        self.y_label = QLabel("Y Coordinate:")
        self.y_input = QLineEdit()

        layout.addWidget(self.x_label)
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y_input)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        if self.automatic_calibration:
            next_button = QPushButton("Next Point")
            next_button.clicked.connect(self.next_point)
            button_layout.addWidget(next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def accept(self):
        """Accepts the input coordinates and closes the dialog."""
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            self.real_coordinates = (x, y)
            super().accept()
        except ValueError:
            self.x_input.setText("")
            self.y_input.setText("")
            self.x_input.setPlaceholderText("Please enter valid numbers")
            self.y_input.setPlaceholderText("Please enter valid numbers")

    def reject(self):
        """Rejects the dialog and cancels the calibration."""
        self.real_coordinates = None
        if self.automatic_calibration:
            self.done(-1)  # signal cancel in automatic calibration
        else:
            super().reject()

    def next_point(self):
        """Handles the next point selection in automatic calibration mode."""
        self.real_coordinates = None
        self.done(1000)  # signal next point
