import cv2
from PyQt5.QtCore import QPointF
from point import Point
import numpy as np

class DataExtraction:
    def __init__(self, calibration, main_window):
        self.data_points = []
        self.temp_points = []  # points automatic extraction
        self.calibration = calibration
        self.main_window = main_window

    def add_data_point(self, scene_pos):
        """Add a data point at the given scene position."""
        real_coordinates = self.calibration.image_to_real_coordinates(scene_pos)
        point = Point(scene_pos, real_coordinates, point_type='data')
        self.data_points.append(point)
        self.main_window.image_view.draw_data_points(self.data_points)
        if self.main_window.interpolation_mode:
            self.main_window.interpolation.interpolate_data(self.data_points)
        self.main_window.show_data_points()

    def delete_data_point(self, index):
        """Deletes a data point at the given index."""
        if 0 <= index < len(self.data_points):
            del self.data_points[index]
            self.main_window.image_view.draw_data_points(self.data_points)
            if self.main_window.interpolation_mode:
                self.main_window.interpolation.interpolate_data(self.data_points)
            self.main_window.show_data_points()

    def get_data_points(self):
        """Returns the list of data points."""
        return self.data_points

    def clear_temp_points(self):
        """Clears the temporary points found during automatic extraction."""
        self.temp_points = []
    def clear_data_points(self):
        """Clears the data points"""
        self.data_points = []
    def automatic_extraction(self, image):
        """Automatically detects data points from the image for visualization."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Enhanced contrast and adaptive thresholding
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(blurred)
        threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Finding contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.clear_temp_points()
        for contour in contours:
            if cv2.contourArea(contour) > 10:  # Minimum area to filter out noise
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    point = QPointF(cX, cY)
                    self.temp_points.append(point)

        self.main_window.image_view.draw_detected_points(self.temp_points)
        return image