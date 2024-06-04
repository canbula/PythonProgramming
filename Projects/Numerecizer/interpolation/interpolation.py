from scipy.interpolate import CubicSpline, Akima1DInterpolator, PchipInterpolator, interp1d
import numpy as np
from PyQt5.QtCore import QPointF
from point import Point

class Interpolation:
    """Class to handle interpolation of data points."""

    def __init__(self, calibration, main_window):
        self.calibration = calibration
        self.main_window = main_window
        self.interpolated_points = []
        self.method = 'linear'  # Default interpolation method

    def set_method(self, method):
        """Sets the interpolation method."""
        if method in ['linear', 'spline', 'polynomial', 'akima', 'pchip', 'quadratic', 'piecewise_linear']:
            self.method = method
        else:
            raise ValueError("Invalid interpolation method. Choose from 'linear', 'spline', 'polynomial', 'akima', 'pchip', 'quadratic', 'piecewise_linear'.")

    def interpolate_data(self, data_points):
        """Interpolates data points using the selected method."""
        if len(data_points) < 2:
            raise ValueError("At least two data points are required for interpolation.")

        valid_points = [point for point in data_points if point.get_real_coordinates() is not None]
        valid_points = sorted(valid_points, key=lambda point: point.get_real_coordinates().x())

        if len(valid_points) < 2:
            raise ValueError("Not enough valid real coordinates for interpolation.")

        x = [point.get_real_coordinates().x() for point in valid_points]
        y = [point.get_real_coordinates().y() for point in valid_points]


        distances = np.diff(x)
        min_distance = np.min(distances) if len(distances) > 0 else 1
        num_points = int((max(x) - min(x)) / min_distance * 40)  # Adjust the factor as needed

        if self.method == 'linear':
            return self.linear_interpolation(x, y, num_points)
        elif self.method == 'spline':
            return self.spline_interpolation(x, y, num_points)
        elif self.method == 'polynomial':
            return self.polynomial_interpolation(x, y, num_points)
        elif self.method == 'akima':
            return self.akima_interpolation(x, y, num_points)
        elif self.method == 'pchip':
            return self.pchip_interpolation(x, y, num_points)
        elif self.method == 'quadratic':
            return self.quadratic_interpolation(x, y, num_points)
        elif self.method == 'piecewise_linear':
            return self.piecewise_linear_interpolation(x, y, num_points)

    def linear_interpolation(self, x, y, num_points):
        """Performs linear interpolation."""
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = np.interp(x_new, x, y)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def spline_interpolation(self, x, y, num_points):
        """Performs spline interpolation and calculates confidence intervals."""
        cs = CubicSpline(x, y)
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = cs(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        lower_bound, upper_bound = self.calculate_confidence_intervals(y_new)
        return self.interpolated_points, x_new, lower_bound, upper_bound

    def polynomial_interpolation(self, x, y, num_points):
        """Performs polynomial interpolation."""
        poly = np.polyfit(x, y, deg=min(len(x)-1, 3))  # Degree 3 polynomial
        poly_func = np.poly1d(poly)
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = poly_func(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def akima_interpolation(self, x, y, num_points):
        """Performs Akima interpolation."""
        akima = Akima1DInterpolator(x, y)
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = akima(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def pchip_interpolation(self, x, y, num_points):
        """Performs Pchip interpolation."""
        pchip = PchipInterpolator(x, y)
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = pchip(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def quadratic_interpolation(self, x, y, num_points):
        """Performs quadratic interpolation."""
        quad = interp1d(x, y, kind='quadratic')
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = quad(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def piecewise_linear_interpolation(self, x, y, num_points):
        """Performs piecewise linear interpolation."""
        piecewise_linear = interp1d(x, y, kind='linear')
        x_new = np.linspace(min(x), max(x), num=num_points)
        y_new = piecewise_linear(x_new)
        self.interpolated_points = [Point(QPointF(x_val, y_val), QPointF(x_val, y_val), point_type='interpolated') for x_val, y_val in zip(x_new, y_new)]
        return self.interpolated_points

    def calculate_confidence_intervals(self, y_new):
        """Calculates confidence intervals for the interpolated points."""
        y_std = np.std(y_new) / np.sqrt(len(y_new))
        confidence_interval = 1.96 * y_std

        lower_bound = y_new - confidence_interval
        upper_bound = y_new + confidence_interval

        return lower_bound, upper_bound

    def calculate_rmse(self, original_points, interpolated_points):
        """Calculates the Root Mean Squared Error (RMSE) for the interpolated points."""
        errors = [(op.get_real_coordinates().y() - ip.get_real_coordinates().y()) ** 2 for op, ip in zip(original_points, interpolated_points)]
        mse = np.mean(errors)
        rmse = np.sqrt(mse)
        return rmse

    def clear_interpolated_points(self):
        """Clears the interpolated points."""
        self.interpolated_points = []
        self.main_window.image_view.clear_interpolated_points()
