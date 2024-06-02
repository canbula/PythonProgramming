import cv2
import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QDialog
from point import Point
from ui.calibration_dialog import CalibrationDialog
import random
class Calibration:
    """Class to manage calibration of images to real-world coordinates."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.calibration_points = []
        self.transformation_matrix = None
        self.inverse_transformation_matrix = None
        self.calibration_done = False
        self.automatic_calibration_mode = False
        self.calibration_cancelled = False

    def add_calibration_point(self, point: QPointF, automatic=False):
        """Adds a calibration point and triggers dialog for real coordinates input."""
        if len(self.calibration_points) < 4:  # Allow selecting 4 calibration points
            point_obj = Point(point, point_type='calibration')
            self.calibration_points.append(point_obj)

            self.main_window.image_view.highlight_point(point_obj)
            self.main_window.image_view.update_scene()
            dialog = CalibrationDialog(self.main_window, automatic_calibration=automatic)
            dialog.setWindowTitle(f"Enter Real Coordinates for Point {len(self.calibration_points)}")
            result = dialog.exec()
            if result == QDialog.Accepted:
                real_x, real_y = dialog.real_coordinates
                point_obj.set_real_coordinates(QPointF(real_x, real_y))
                self.main_window.image_view.delete_highlight(point_obj)
                self.main_window.image_view.draw_calibration_points(self.calibration_points)
                if len(self.calibration_points) == 4:  # Calculate, refine transformation matrix
                    self.calculate_transformation_matrix()
                    self.refine_calibration()
            elif result == 1000:  # Next point
                self.calibration_points.pop()
                self.main_window.image_view.delete_highlight(point_obj)
                new_point = self.select_random_point()
                if new_point is not None and not self.calibration_cancelled:
                    self.add_calibration_point(new_point, automatic=True)
            else:
                self.calibration_points.pop()
                self.main_window.image_view.delete_highlight(point_obj)
                if automatic:
                    self.calibration_cancelled = True  # Mark calibration as cancelled
                    self.clear_calibration_points()

    def clear_calibration_points(self):
        """Clears all calibration points."""
        self.main_window.image_view.clear_calibration_points()
        self.calibration_points = []
        self.calibration_done = False

    def calculate_transformation_matrix(self):
        """Calculates the transformation matrix based on calibration points."""
        if len(self.calibration_points) != 4:
            raise ValueError("Exactly 4 calibration points are required to calculate the transformation matrix.")

        image_points = np.array(
            [[p.get_image_coordinates().x(), p.get_image_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)
        real_coords = np.array(
            [[p.get_real_coordinates().x(), p.get_real_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)

        self.transformation_matrix, _ = cv2.findHomography(image_points, real_coords)
        self.inverse_transformation_matrix = np.linalg.inv(self.transformation_matrix)

        self.calibration_done = True
        self.main_window.interpolationAction.setEnabled(True)

    def refine_calibration(self, iterations=500, termination_eps=1e-6):
        """Refines the calibration matrix using iterative optimization."""
        if len(self.calibration_points) != 4:
            raise ValueError("Exactly 4 calibration points are required to refine the calibration matrix.")

        image_points = np.array(
            [[p.get_image_coordinates().x(), p.get_image_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)
        real_coords = np.array(
            [[p.get_real_coordinates().x(), p.get_real_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)

        self.transformation_matrix, _ = cv2.findHomography(image_points, real_coords, method=cv2.RANSAC, ransacReprojThreshold=5.0, maxIters=iterations, confidence=0.99)
        self.inverse_transformation_matrix = np.linalg.inv(self.transformation_matrix)

        self.calibration_done = True
        self.main_window.interpolationAction.setEnabled(True)

    def transform_points(self, data_points):
        """Transforms data points using the calibration matrix."""
        if not self.calibration_done:
            raise RuntimeError("Calibration is not complete. Please complete calibration before transforming points.")

        transformed_points = []
        for point in data_points:
            img_coords = np.array([[point.get_image_coordinates().x(), point.get_image_coordinates().y(), 1.0]],
                                  dtype=np.float32)
            real_coords = cv2.perspectiveTransform(np.array([img_coords]), self.transformation_matrix)
            point.set_real_coordinates(QPointF(real_coords[0][0][0], real_coords[0][0][1]))
            transformed_points.append(point)

        return transformed_points

    def inverse_transform_point(self, x, y):
        """Transforms real-world coordinates back to image coordinates using the inverse calibration matrix."""
        if self.inverse_transformation_matrix is None:
            raise ValueError("Inverse transformation matrix has not been calculated yet.")

        real_coords = np.array([[x, y]], dtype=np.float32).reshape(-1, 1, 2)
        img_coords = cv2.perspectiveTransform(real_coords, self.inverse_transformation_matrix)

        return QPointF(img_coords[0][0][0], img_coords[0][0][1])

    def image_to_real_coordinates(self, point):
        """Transforms image coordinates to real-world coordinates using the calibration matrix."""
        if not self.calibration_done:
            raise RuntimeError("Calibration is not complete. Please complete calibration before transforming points.")

        img_coords = np.array([[point.x(), point.y()]], dtype=np.float32).reshape(-1, 1, 2)
        real_coords = cv2.perspectiveTransform(img_coords, self.transformation_matrix)
        return QPointF(real_coords[0][0][0], real_coords[0][0][1])

    def refine_calibration(self, iterations=500, termination_eps=1e-6):
        """Refines the calibration matrix using iterative optimization."""
        if len(self.calibration_points) != 4:
            raise ValueError("Exactly 4 calibration points are required to refine the calibration matrix.")

        image_points = np.array(
            [[p.get_image_coordinates().x(), p.get_image_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)
        real_coords = np.array(
            [[p.get_real_coordinates().x(), p.get_real_coordinates().y()] for p in self.calibration_points],
            dtype=np.float32)

        # Use cv2.findHomography with RANSAC to refine the transformation matrix
        self.transformation_matrix, _ = cv2.findHomography(image_points, real_coords, method=cv2.RANSAC, ransacReprojThreshold=5.0, maxIters=iterations, confidence=0.99)
        self.inverse_transformation_matrix = np.linalg.inv(self.transformation_matrix)

        self.calibration_done = True
        self.main_window.interpolationAction.setEnabled(True)
    def advanced_corner_detection(self, image):
        """Improves corner detection using optimized algorithms."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Enhanced contrast and adaptive thresholding
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Line detection using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=10)

        line_img = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Find line intersections
        intersections = self.find_intersections(lines)

        # Corner detection using Shi-Tomasi algorithm on the edge image
        corners = cv2.goodFeaturesToTrack(edges, maxCorners=100, qualityLevel=0.01, minDistance=10)
        corners = np.float32(corners)

        # Refining corner locations using cornerSubPix for sub-pixel accuracy
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
        corners = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)

        # Only keep corners that are close to detected lines and intersections
        refined_corners = []
        for corner in corners:
            x, y = corner.ravel()
            if self.is_near_line(x, y, lines) or self.is_near_intersection(x, y, intersections):
                refined_corners.append(QPointF(x, y))
                self.main_window.image_view.draw_detected_corners(refined_corners)

        self.main_window.image_view.set_image(image)
        self.main_window.update_image()

        return refined_corners

    def is_near_line(self, x, y, lines, threshold=5):
        """Checks if a point (x, y) is near any of the detected lines."""
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                distance = self.point_line_distance(x, y, x1, y1, x2, y2)
                if distance < threshold:
                    return True
        return False

    def point_line_distance(self, px, py, x1, y1, x2, y2):
        """Calculates the minimum distance from a point to a line segment."""
        line_mag = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if line_mag < 1e-10:
            return np.sqrt((px - x1) ** 2 + (py - y1) ** 2)
        u = ((px - x1) * (x2 - x1) + (py - y1)) / line_mag ** 2
        if u < 0 or u > 1:
            ix = min(max(x1, x2), max(px, px))
            iy = min(max(y1, y2), max(py, py))
        else:
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
        return np.sqrt((px - ix) ** 2 + (py - iy) ** 2)

    def find_intersections(self, lines):
        """Finds intersections between lines."""
        intersections = []
        if lines is not None:
            for i in range(len(lines)):
                for j in range(i + 1, len(lines)):
                    x1, y1, x2, y2 = lines[i][0]
                    x3, y3, x4, y4 = lines[j][0]
                    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    if denom != 0:
                        intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
                        intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
                        intersections.append((intersect_x, intersect_y))
        return intersections

    def is_near_intersection(self, x, y, intersections, threshold=5):
        """Checks if a point (x, y) is near any of the detected intersections."""
        for intersect_x, intersect_y in intersections:
            distance = np.sqrt((x - intersect_x) ** 2 + (y - intersect_y) ** 2)
            if distance < threshold:
                return True
        return False

    def automatic_calibration(self, image):
        """Automatically calibrates the image using enhanced corner detection."""
        print("Starting automatic calibration...")
        self.automatic_calibration_mode = True
        self.calibration_cancelled = False  # Reset cancellation flag
        corners = self.advanced_corner_detection(image)

        if len(corners) >= 10:
            corners = random.sample(corners, 4)  # Take 4 random corners
            self.calibration_points = []
            for corner in corners:
                if not self.calibration_cancelled:
                    self.add_calibration_point(corner, automatic=True)
            if len(self.calibration_points) == 4:
                self.calculate_transformation_matrix()
            else:
                self.clear_calibration_points()
        else:
            print("Not enough corners detected for calibration.")
        self.automatic_calibration_mode = False

    def select_random_point(self):
        """Selects a random point from detected corners for automatic calibration."""
        corners = self.advanced_corner_detection(self.main_window.image_processor.image)
        if corners:
            return random.choice(corners)
        return None
