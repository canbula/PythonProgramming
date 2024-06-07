from PyQt5.QtCore import QPointF


class Point:
    """Class to represent a point in both image and real-world coordinates."""

    def __init__(self, image_coordinates, real_coordinates=None, point_type='data'):
        self.image_coordinates = image_coordinates
        self.real_coordinates = real_coordinates if real_coordinates is not None else QPointF()
        self.point_type = point_type

    def set_image_coordinates(self, coordinates: QPointF):
        """Sets the image coordinates of the point."""
        self.image_coordinates = coordinates

    def get_image_coordinates(self) -> QPointF:
        """Returns the image coordinates of the point."""
        return self.image_coordinates

    def set_real_coordinates(self, coordinates: QPointF):
        """Sets the real-world coordinates of the point."""
        self.real_coordinates = coordinates

    def get_real_coordinates(self) -> QPointF:
        """Returns the real-world coordinates of the point."""
        return self.real_coordinates
