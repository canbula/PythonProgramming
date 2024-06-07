from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QLabel, QInputDialog, QMenu, QRubberBand, QApplication, QGraphicsLineItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPen, QBrush, QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF, QRectF, QRect, QSize
import numpy as np
from point import Point
import calibration.calibration
class ImageView(QGraphicsView):
    """Class to handle displaying images and interacting with points on the image."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap_item = None
        self.zoom_factor = 1
        self.main_window = parent
        self.calibration_points_graphics = []
        self.data_points_graphics = []
        self.interpolated_points_graphics = []
        self.detected_points_graphics = []
        self.highlighted_points = []
        self.perspective_points = []
        self.info_label = QLabel(self)
        self.info_label.setStyleSheet("QLabel { background-color : white; color : black; }")
        self.info_label.setFixedWidth(200)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.hide()

        # Selection tool
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPointF()
        self.selection_mode = True# Default
        self.selected_items = []
        self.dragging = False
        self.drag_start_position = None

        # Magnifier tool
        self.magnifier = QGraphicsRectItem()
        self.magnifier.setRect(0, 0, 20, 20)
        self.magnifier.setPen(QPen(Qt.green, 2))
        self.magnifier.setVisible(False)
        self.scene.addItem(self.magnifier)

    def set_image(self, image):
        """Sets and displays the given image in the view."""
        if len(image.shape) == 3:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        elif len(image.shape) == 2:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:
            raise ValueError("Unsupported image format")

        self.pixmap = QPixmap.fromImage(q_image)
        if self.pixmap_item is None:
            self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.pixmap_item)
            self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        else:
            self.pixmap_item.setPixmap(self.pixmap)
        self.update_scene()

    def wheelEvent(self, event):
        """Handles zooming in and out using the mouse wheel."""
        if self.pixmap_item:
            degrees = event.angleDelta().y() / 8
            steps = degrees / 15
            self.zoom_factor *= 1.1 ** steps
            self.scale(1.1 ** steps, 1.1 ** steps)

    def mousePressEvent(self, event):
        """Handles mouse press events to add points or perform perspective correction."""
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            if not event.modifiers() & Qt.ControlModifier:
                self.clear_selection()
            if self.selection_mode:
                self.rubber_band.setGeometry(QRect(self.origin, QSize()))
                self.rubber_band.show()
            else:
                scene_pos = self.mapToScene(event.pos())
                if self.pixmap_item and self.pixmap_item.contains(scene_pos):
                    if self.main_window.calibration_mode:
                        self.main_window.calibration.add_calibration_point(scene_pos)
                        self.update_scene()
                    elif self.main_window.extraction_mode:
                        self.main_window.extraction.add_data_point(scene_pos)
                        self.update_scene()
                    elif self.main_window.perspective_mode:
                        self.add_perspective_point(scene_pos)
                        if len(self.perspective_points) == 4:
                            self.main_window.correct_perspective(self.perspective_points)
                            self.perspective_points.clear()
                            self.info_label.hide()
                        else:
                            self.main_window.update_perspective_info()
                        self.update_scene()
                    elif self.main_window.feature_detection_mode:
                        for point in self.main_window.extraction.temp_points:
                            if point.x() - 3 <= scene_pos.x() <= point.x() + 3 and \
                                    point.y() - 3 <= scene_pos.y() <= point.y() + 3:
                                self.main_window.extraction.add_data_point(point)
                                self.main_window.show_data_points()
                                self.update_scene()
                                break
        elif event.button() == Qt.RightButton:
            self.origin = event.pos()
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())
            if isinstance(item, QGraphicsEllipseItem):
                self.selected_items = [item]
                self.drag_start_position = event.pos()
            else:
                self.selected_items = []

    def mouseMoveEvent(self, event):
        if self.selection_mode and not self.rubber_band.isHidden():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        elif self.selected_items and self.drag_start_position and (
                event.pos() - self.drag_start_position).manhattanLength() > QApplication.startDragDistance():
            self.dragging = True
            new_pos = self.mapToScene(event.pos())
            for item in self.selected_items:
                item.setPos(new_pos - item.boundingRect().center())
                point = item.data(0)
                if point:
                    point.set_image_coordinates(new_pos)
            self.update_scene()
        if self.magnifier.isVisible():
            self.update_magnifier(event)

    def mouseReleaseEvent(self, event):
        if self.selection_mode and event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            rect = self.rubber_band.geometry()
            selection_rect = self.mapToScene(rect).boundingRect()
            selected_items = self.scene.items(selection_rect)
            self.clear_selection()
            for item in selected_items:
                if isinstance(item, QGraphicsEllipseItem):
                    point = item.data(0)
                    if isinstance(point, Point):
                        self.highlight_point(point)
                        self.selected_items.append(item)
            self.update_scene()
        elif event.button() == Qt.RightButton:
            self.selected_items = []
            self.dragging = False
            self.drag_start_position = None

    def update_magnifier(self, event):
        """Updates the position and content of the magnifier."""
        if event.buttons() & Qt.MiddleButton:
            self.magnifier.setVisible(True)
            scene_pos = self.mapToScene(event.pos())
            self.magnifier.setRect(scene_pos.x() - 50, scene_pos.y() - 50, 100, 100)
            self.update_magnifier_content(scene_pos)
        else:
            self.magnifier.setVisible(False)

    def update_magnifier_content(self, scene_pos):
        """Updates the content inside the magnifier."""
        if self.pixmap_item:
            pixmap = self.pixmap_item.pixmap()
            rect = self.magnifier.rect()
            magnified_image = pixmap.copy(rect.toRect()).scaled(rect.width() * 2, rect.height() * 2, Qt.KeepAspectRatio)
            painter = QPainter(self.pixmap_item.pixmap())
            painter.setOpacity(0.5)
            painter.drawPixmap(rect.topLeft(), magnified_image)
            painter.end()
        self.update()

    def clear_selection(self):
        """Clears the current selection."""
        for item in self.selected_items:
            point = item.data(0)
            if isinstance(point, Point):
                self.delete_highlight(point)
        self.selected_items = []
        self.update()

    def add_perspective_point(self, point):
        """Adds a point for perspective correction."""
        ellipse = QGraphicsEllipseItem(point.x() - 5, point.y() - 5, 10, 10)
        ellipse.setBrush(QBrush(Qt.red))
        ellipse.setPen(QPen(Qt.red))
        self.scene.addItem(ellipse)
        self.perspective_points.append(point)
        self.update()

    def clear_perspective_points(self):
        """Clears all perspective points from the image."""
        for point in self.perspective_points:
            items = self.scene.items(QRectF(point.x() - 5, point.y() - 5, 10, 10))
            for item in items:
                if isinstance(item, QGraphicsEllipseItem):
                    self.scene.removeItem(item)
        self.perspective_points = []
        self.update_scene()
    def draw_calibration_points(self, calibration_points):
        """Draws calibration points on the image."""
        for point_graphic in self.calibration_points_graphics:
            self.scene.removeItem(point_graphic)
        self.calibration_points_graphics = []
        for i, point in enumerate(calibration_points):
            coords = point.get_image_coordinates()
            x = coords.x()
            y = coords.y()
            point_graphic = self.scene.addEllipse(x - 3, y - 3, 6, 6, QPen(Qt.red), QBrush(Qt.red))
            text = self.scene.addText(str(i + 1), QFont('Arial', 10))
            text.setPos(x + 5, y - 10)
            text.setDefaultTextColor(Qt.red)
            self.calibration_points_graphics.append(point_graphic)
            self.calibration_points_graphics.append(text)
        self.update()

    def draw_detected_corners(self, corners):
        """Draws detected corners on the image."""
        for point_graphic in self.detected_points_graphics:
            self.scene.removeItem(point_graphic)
        self.detected_points_graphics = []
        for corner in corners:
            x = corner.x()
            y = corner.y()
            point_graphic = self.scene.addEllipse(x - 1.5, y - 1.5, 3, 3, QPen(Qt.green), QBrush(Qt.green))
            self.detected_points_graphics.append(point_graphic)
        self.update()

    def draw_data_points(self, data_points):
        """Draws data points on the image."""
        for point_graphic in self.data_points_graphics:
            self.scene.removeItem(point_graphic)
        self.data_points_graphics = []
        for point in data_points:
            x = point.get_image_coordinates().x()
            y = point.get_image_coordinates().y()
            point_graphic = self.scene.addEllipse(x - 3, y - 3, 6, 6, QPen(Qt.blue), QBrush(Qt.blue))
            point_graphic.setData(0, point)
            self.data_points_graphics.append(point_graphic)
        self.update()

    def draw_interpolated_points(self, points):
        """Draws interpolated points on the image."""
        pen = QPen(Qt.green, 4)
        for point in points:
            real_coords = point.get_real_coordinates()
            image_coords = self.main_window.calibration.inverse_transform_point(real_coords.x(), real_coords.y())
            ellipse = self.scene.addEllipse(image_coords.x() - 2,
                                            image_coords.y() - 2,
                                            4, 4, pen)
            ellipse.setData(0, point)
        self.update()

    def draw_confidence_intervals(self, x_new, lower_bound, upper_bound):
        """Draws confidence intervals for the interpolated points."""
        pen = QPen(QColor(255, 0, 0, 127), 2, Qt.SolidLine)
        for x, y_low, y_high in zip(x_new, lower_bound, upper_bound):
            low_point = self.main_window.calibration.inverse_transform_point(x, y_low)
            high_point = self.main_window.calibration.inverse_transform_point(x, y_high)
            line = QGraphicsLineItem(low_point.x(), low_point.y(), high_point.x(), high_point.y())
            line.setPen(pen)
            self.scene.addItem(line)
        self.update()

    def clear_interpolated_points(self):
        """Clears interpolated points from the image."""
        for item in self.scene.items():
            if isinstance(item, QGraphicsEllipseItem) and item.pen().color() == Qt.green:
                self.scene.removeItem(item)
            if isinstance(item, QGraphicsLineItem) and item.pen().color() == QColor(255, 0, 0, 127):
                self.scene.removeItem(item)
        self.update()

    def draw_detected_points(self, detected_points):
        """Draws detected points on the image."""
        for point_graphic in self.detected_points_graphics:
            self.scene.removeItem(point_graphic)
        self.detected_points_graphics = []
        for point in detected_points:
            if isinstance(point, QPointF):
                x = point.x()
                y = point.y()
            else:
                point_coords = point.get_image_coordinates()
                x = point_coords.x()
                y = point_coords.y()
            point_graphic = self.scene.addEllipse(x - 2, y - 2, 4, 4, QPen(Qt.green), QBrush(Qt.green))
            self.detected_points_graphics.append(point_graphic)

    def highlight_point(self, point):
        """Highlights a specific point by adding it to the highlighted points list."""
        self.highlighted_points.append(point)
        self.update_scene()

    def draw_highlights(self):
        """Draws highlighted points on the image."""
        for point in self.highlighted_points:
            coords = point.get_image_coordinates()
            ellipse = QGraphicsEllipseItem(coords.x() - 5, coords.y() - 5, 10, 10)
            ellipse.setBrush(QBrush(Qt.yellow))
            ellipse.setPen(QPen(Qt.yellow))
            self.scene.addItem(ellipse)
        self.update()

    def delete_highlight(self, point):
        """Deletes a specific highlight from the image."""
        new_highlighted_points = []
        for highlighted_point in self.highlighted_points:
            if highlighted_point != point:
                new_highlighted_points.append(highlighted_point)
            else:
                coords = highlighted_point.get_image_coordinates()
                items = self.scene.items(QRectF(coords.x() - 5, coords.y() - 5, 10, 10))
                for item in items:
                    if isinstance(item, QGraphicsEllipseItem):
                        self.scene.removeItem(item)
        self.highlighted_points = new_highlighted_points
        self.update_scene()

    def clear_highlights(self):
        """Clears all highlighted points from the image."""
        for point in self.highlighted_points:
            coords = point.get_image_coordinates()
            items = self.scene.items(QRectF(coords.x() - 5, coords.y() - 5, 10, 10))
            for item in items:
                if isinstance(item, QGraphicsEllipseItem):
                    self.scene.removeItem(item)
        self.highlighted_points = []
        self.update_scene()

    def clear_calibration_points(self):
        """Clears all calibration points from the image."""
        for point_graphic in self.calibration_points_graphics:
            self.scene.removeItem(point_graphic)
        self.calibration_points_graphics = []
        self.clear_highlights()
        self.update()

    def clear_detected_points(self):
        """Clears all detected points from the scene."""
        for point_graphic in self.detected_points_graphics:
            self.scene.removeItem(point_graphic)
        self.detected_points_graphics = []

    def update_scene(self):
        """Updates the scene with the current points and image."""
        if self.main_window.feature_detection_mode:
            self.draw_detected_points(self.main_window.extraction.temp_points)
        else:
            self.main_window.extraction.clear_temp_points()
            self.clear_detected_points()
        self.draw_highlights()
        self.draw_calibration_points(self.main_window.calibration.calibration_points)
        self.draw_data_points(self.main_window.extraction.data_points)
        self.draw_interpolated_points(self.main_window.interpolation.interpolated_points)

        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def show_info_label(self, text):
        """Displays an informational label."""
        self.info_label.setText(text)
        self.info_label.adjustSize()
        self.info_label.show()

    def contextMenuEvent(self, event):
        """Creates a context menu for editing or deleting data points."""
        scene_pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(scene_pos, self.transform())

        if isinstance(item, QGraphicsEllipseItem):
            context_menu = QMenu(self)
            edit_action = context_menu.addAction("Edit Point")
            delete_action = context_menu.addAction("Delete Point")

            action = context_menu.exec_(self.mapToGlobal(event.pos()))

            if action == edit_action:
                self.main_window.edit_data_point(item)
            elif action == delete_action:
                self.main_window.delete_data_point(item)

    def delete_point(self, item):
        """Deletes the selected data point."""
        point = item.data(0)
        if point:
            self.scene.removeItem(item)
            self.main_window.extraction.data_points.remove(point)
            self.main_window.image_view.delete_highlight(point)
            self.update_scene()
        self.update()

    def reset_view(self):
        """Resets the view to the original state (centered and zoom reset)."""
        self.resetTransform()
        self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.zoom_factor = 1