from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog, QListWidget,
                             QListWidgetItem, QInputDialog, QMessageBox, QToolTip, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QWidget, QDockWidget, QStatusBar, QLabel, QPushButton,QGraphicsEllipseItem)
from PyQt5.QtGui import QCursor, QFont, QPen, QIcon
from PyQt5.QtCore import Qt, QPointF
from ui.image_view import ImageView
from image_processing import ImageProcessor
from calibration import Calibration
from data_extraction import DataExtraction
from interpolation import Interpolation
from export import DataExporter
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import qdarkstyle
from ui.plot_window import PlotWindow
from point import Point
class MainWindow(QMainWindow):
    """Main application window class."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = QApplication.instance()
        self.image_processor = ImageProcessor()
        self.calibration = Calibration(self)
        self.extraction = DataExtraction(self.calibration, self)
        self.interpolation = Interpolation(self.calibration, self)
        self.data_exporter = DataExporter()

        self.calibration_mode = False
        self.extraction_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.feature_detection_mode = False

        self.original_image = None
        self.undo_stack = []
        self.redo_stack = []

        self.initUI()

    def initUI(self):
        """Initializes the user interface components."""
        self.setWindowTitle('Numericizer')
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags( Qt.Window)

        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setStyleSheet("""
            QWidget#title_bar {
                background-color: #444;
                color: white;}""")

        self.title_bar.setFixedHeight(30)

        self.title_label = QLabel("Numericizer", self.title_bar)
        self.title_label.setStyleSheet("margin-left: 10px;")

        self.minimize_button = QPushButton("-", self.title_bar)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.maximize_button = QPushButton("⬜", self.title_bar)
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)

        self.close_button = QPushButton("✕", self.title_bar)
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.maximize_button)
        title_layout.addWidget(self.close_button)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.title_bar)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        self.image_view = ImageView(self)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()
        self.data_points_list = self.init_data_points_list()
        left_layout.addWidget(self.data_points_list)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.image_view)

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createDockWidget()

        self.setMouseTracking(True)
        self.old_position = self.pos()

    def mousePressEvent(self, event):
        """Handles mouse press events for moving the window."""
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPos()

    def mouseMoveEvent(self, event):
        """Handles mouse move events for moving the window."""
        if event.buttons() == Qt.LeftButton:
            delta = QPointF(event.globalPos() - self.old_position)
            self.move(self.x() + int(delta.x()), self.y() + int(delta.y()))
            self.old_position = event.globalPos()

    def toggle_maximize_restore(self):
        """Toggles between maximized and normal states."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def createActions(self):
        """Creates the actions for the application."""
        self.openAction = QAction(QIcon('icons/open.png'), '&Open Image', self)
        self.openAction.setToolTip('Open an image file for processing')
        self.openAction.triggered.connect(self.open_image)

        self.exportCsvAction = QAction(QIcon('icons/export_csv.png'), '&Export as CSV', self)
        self.exportCsvAction.setToolTip('Export the extracted data points as a CSV file')
        self.exportCsvAction.triggered.connect(self.export_data_as_csv)

        self.exportJsonAction = QAction(QIcon('icons/export_json.png'), '&Export as JSON', self)
        self.exportJsonAction.setToolTip('Export the extracted data points as a JSON file')
        self.exportJsonAction.triggered.connect(self.export_data_as_json)

        self.calibrationAction = QAction(QIcon('icons/calibrate.png'), '&Calibrate Axes', self)
        self.calibrationAction.setToolTip('Calibrate the axes using known reference points')
        self.calibrationAction.setEnabled(False)
        self.calibrationAction.triggered.connect(self.toggle_calibration_mode)

        self.automaticCalibrationAction = QAction(QIcon('icons/automatic_calibration.png'), '&Automatic Calibration', self)
        self.automaticCalibrationAction.setToolTip('Automatically calibrate the axes')
        self.automaticCalibrationAction.setEnabled(False)
        self.automaticCalibrationAction.triggered.connect(self.automatic_calibration)

        self.extractionAction = QAction(QIcon('icons/extract.png'), '&Extract Data', self)
        self.extractionAction.setToolTip('Extract data points from the image')
        self.extractionAction.setEnabled(False)
        self.extractionAction.triggered.connect(self.toggle_extraction_mode)

        self.interpolationAction = QAction(QIcon('icons/interpolate.png'), '&Interpolate Data', self)
        self.interpolationAction.setToolTip('Interpolate data points between the extracted points')
        self.interpolationAction.setEnabled(False)
        self.interpolationAction.triggered.connect(self.toggle_interpolation_mode)

        self.detectedPointsAction = QAction(QIcon('icons/feature_detection.png'), '&Advanced Feature Detection(Experimental)', self)
        self.detectedPointsAction.setToolTip('Detect advanced features like lines and intersections in the image')
        self.detectedPointsAction.setEnabled(False)
        self.detectedPointsAction.triggered.connect(self.toggle_feature_detection_mode)

        self.histogramAction = QAction(QIcon('icons/histogram.png'), '&Equalize Histogram', self)
        self.histogramAction.setToolTip('Apply histogram equalization to the image')
        self.histogramAction.setEnabled(False)
        self.histogramAction.triggered.connect(self.equalize_histogram)

        self.edgeAction = QAction(QIcon('icons/edge_detection.png'), '&Edge Detection', self)
        self.edgeAction.setToolTip('Apply edge detection to the image')
        self.edgeAction.setEnabled(False)
        self.edgeAction.triggered.connect(self.edge_detection)

        self.denoiseAction = QAction(QIcon('icons/denoise.png'), '&Denoise Image', self)
        self.denoiseAction.setToolTip('Apply denoising to the image')
        self.denoiseAction.setEnabled(False)
        self.denoiseAction.triggered.connect(self.denoise_image)

        self.perspectiveAction = QAction(QIcon('icons/perspective.png'), '&Correct Perspective', self)
        self.perspectiveAction.setToolTip('Correct the perspective of the image')
        self.perspectiveAction.setEnabled(False)
        self.perspectiveAction.triggered.connect(self.toggle_perspective_mode)

        self.rotateAction = QAction(QIcon('icons/rotate.png'), '&Rotate Image', self)
        self.rotateAction.setToolTip('Rotate the image by a specified angle')
        self.rotateAction.setEnabled(False)
        self.rotateAction.triggered.connect(self.rotate_image)

        self.deletePointAction = QAction('&Delete Data Point', self)
        self.deletePointAction.setToolTip('Delete a selected data point')
        self.deletePointAction.triggered.connect(self.delete_data_point)

        self.selectionToolAction = QAction(QIcon('icons/selection.png'), '&Selection Tool', self)
        self.selectionToolAction.setToolTip('Enable selection tool')
        self.selectionToolAction.triggered.connect(self.enable_selection_tool)

        self.undoAction = QAction(QIcon('icons/undo.png'), '&Undo', self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setToolTip('Undo the last action')
        self.undoAction.triggered.connect(self.undo)

        self.redoAction = QAction(QIcon('icons/redo.png'), '&Redo', self)
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.setToolTip('Redo the last undone action')
        self.redoAction.triggered.connect(self.redo)

        self.plotPointsAction = QAction(QIcon('icons/plot.png'), '&Plot Data Points', self)
        self.plotPointsAction.setToolTip('Plot the extracted data points')
        self.plotPointsAction.triggered.connect(self.open_plot_window)

        self.resetViewAction = QAction(QIcon('icons/reset_view.png'), 'Reset View', self)
        self.resetViewAction.triggered.connect(self.reset_view)

        self.magnifierAction = QAction(QIcon('icons/magnifier.png'), 'Magnifier Tool', self)
        self.magnifierAction.setToolTip('Activate magnifier tool')
        self.magnifierAction.triggered.connect(self.toggle_magnifier_mode)

        self.toggleThemeAction = QAction('&Toggle Dark Theme', self)
        self.toggleThemeAction.setToolTip('Toggle between dark and light themes')
        self.toggleThemeAction.setCheckable(True)
        self.toggleThemeAction.triggered.connect(self.toggle_theme)

        self.resetAction = QAction(QIcon('icons/reset.png'), '&Reset Application', self)
        self.resetAction.setToolTip('Reset the application to its initial state')
        self.resetAction.triggered.connect(self.reset_application)
    def createMenus(self):
        """Creates the menus for the application."""
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        exportMenu = fileMenu.addMenu('Export As')
        exportMenu.addAction(self.exportCsvAction)
        exportMenu.addAction(self.exportJsonAction)
        fileMenu.addAction(self.resetAction)

        toolsMenu = menubar.addMenu('&Tools')
        toolsMenu.addAction(self.calibrationAction)
        toolsMenu.addAction(self.automaticCalibrationAction)
        toolsMenu.addAction(self.extractionAction)
        toolsMenu.addAction(self.interpolationAction)
        toolsMenu.addAction(self.detectedPointsAction)
        toolsMenu.addAction(self.deletePointAction)
        toolsMenu.addAction(self.selectionToolAction)
        toolsMenu.addAction(self.undoAction)
        toolsMenu.addAction(self.redoAction)

        imageProcessingMenu = menubar.addMenu('&Image Processing')
        imageProcessingMenu.addAction(self.histogramAction)
        imageProcessingMenu.addAction(self.edgeAction)
        imageProcessingMenu.addAction(self.denoiseAction)
        imageProcessingMenu.addAction(self.perspectiveAction)
        imageProcessingMenu.addAction(self.rotateAction)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(self.plotPointsAction)
        viewMenu.addAction(self.resetViewAction)
        viewMenu.addAction(self.magnifierAction)
        viewMenu.addAction(self.toggleThemeAction)

        interpolationMenu = menubar.addMenu('Interpolation Method')
        self.add_interpolation_methods(interpolationMenu)

    def toggle_magnifier_mode(self):
        """Toggles the magnifier mode."""
        if self.image_view.magnifier.isVisible():
            self.image_view.magnifier.setVisible(False)
            self.status_bar.showMessage("Magnifier tool deactivated.", 5000)
            self.image_view.setCursor(Qt.ArrowCursor)
        else:
            # Disable other modes
            self.calibration_mode = False
            self.extraction_mode = False
            self.interpolation_mode = False
            self.perspective_mode = False
            self.feature_detection_mode = False
            self.image_view.selection_mode = False

            self.image_view.clear_selection()


            self.image_view.magnifier.setVisible(True)
            self.status_bar.showMessage("Magnifier tool activated. Use middle mouse button to magnify.", 5000)
            self.image_view.setCursor(Qt.CrossCursor)

    def toggle_theme(self):
        """Toggles the application theme between dark and light."""
        if self.toggleThemeAction.isChecked():
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.status_bar.showMessage("Dark theme activated.", 5000)
        else:
            self.app.setStyleSheet("")
            self.status_bar.showMessage("Light theme activated.", 5000)
    def createToolBars(self):
        """Creates the toolbars for the application."""
        mainToolBar = self.addToolBar('Main')
        mainToolBar.addAction(self.openAction)
        mainToolBar.addAction(self.calibrationAction)
        mainToolBar.addAction(self.automaticCalibrationAction)
        mainToolBar.addAction(self.extractionAction)
        mainToolBar.addAction(self.interpolationAction)
        mainToolBar.addAction(self.detectedPointsAction)
        mainToolBar.addAction(self.histogramAction)
        mainToolBar.addAction(self.edgeAction)
        mainToolBar.addAction(self.denoiseAction)
        mainToolBar.addAction(self.perspectiveAction)
        mainToolBar.addAction(self.rotateAction)
        mainToolBar.addAction(self.resetAction)
        mainToolBar.addAction(self.magnifierAction)

    def createDockWidget(self):
        """Creates a dock widget for additional tools."""
        dockWidget = QDockWidget('Tools', self)
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        toolWidget = QWidget()
        dockWidget.setWidget(toolWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def add_interpolation_methods(self, interpolationMenu):
        """Adds interpolation methods to the interpolation menu."""
        linearAction = QAction('Linear', self)
        splineAction = QAction('Spline', self)
        polynomialAction = QAction('Polynomial', self)
        akimaAction = QAction('Akima', self)
        pchipAction = QAction('Pchip', self)
        quadraticAction = QAction('Quadratic', self)
        piecewiseLinearAction = QAction('Piecewise Linear', self)

        linearAction.triggered.connect(lambda: self.set_interpolation_method('linear'))
        splineAction.triggered.connect(lambda: self.set_interpolation_method('spline'))
        polynomialAction.triggered.connect(lambda: self.set_interpolation_method('polynomial'))
        akimaAction.triggered.connect(lambda: self.set_interpolation_method('akima'))
        pchipAction.triggered.connect(lambda: self.set_interpolation_method('pchip'))
        quadraticAction.triggered.connect(lambda: self.set_interpolation_method('quadratic'))
        piecewiseLinearAction.triggered.connect(lambda: self.set_interpolation_method('piecewise_linear'))

        interpolationMenu.addAction(linearAction)
        interpolationMenu.addAction(splineAction)
        interpolationMenu.addAction(polynomialAction)
        interpolationMenu.addAction(akimaAction)
        interpolationMenu.addAction(pchipAction)
        interpolationMenu.addAction(quadraticAction)
        interpolationMenu.addAction(piecewiseLinearAction)

    def init_data_points_list(self):
        data_points_list = QListWidget(self)
        data_points_list.setGeometry(800, 50, 200, 500)
        data_points_list.itemDoubleClicked.connect(self.edit_data_point)
        return data_points_list

    def enable_selection_tool(self):
        """Enables the selection tool."""
        self.calibration_mode = False
        self.extraction_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.feature_detection_mode = False
        self.image_view.selection_mode = True
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.image_view.clear_selection()

    def open_image(self):
        """Opens an image file and displays it."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)
        if file_path:
            self.image_processor.load_image(file_path)
            self.original_image = self.image_processor.image.copy()
            self.image_view.set_image(self.image_processor.image)

            self.calibrationAction.setEnabled(True)
            self.automaticCalibrationAction.setEnabled(True)
            self.extractionAction.setEnabled(True)
            self.histogramAction.setEnabled(True)
            self.edgeAction.setEnabled(True)
            self.denoiseAction.setEnabled(True)
            self.perspectiveAction.setEnabled(True)
            self.rotateAction.setEnabled(True)
            self.detectedPointsAction.setEnabled(True)
            self.status_bar.showMessage(f"Image {os.path.basename(file_path)} loaded.", 5000)

    def set_interpolation_method(self, method):
        """Sets the interpolation method in the Interpolation class."""
        try:
            self.interpolation.set_method(method)
            QMessageBox.information(self, "Interpolation Method", f"Interpolation method set to {method}.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def enable_selection_tool(self):
        """Enables the selection tool."""
        self.calibration_mode = False
        self.extraction_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.feature_detection_mode = False
        self.image_view.selection_mode = True
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.image_view.clear_selection()

    def toggle_extraction_mode(self):
        """Toggles the data extraction mode."""
        if not self.calibration.calibration_done or len(self.calibration.calibration_points) < 4:
            QMessageBox.warning(self, "Calibration Required",
                                "Calibration is required before extraction. Please calibrate at least 4 points.")
            return

        self.image_view.update_scene()
        self.image_view.update()
        self.extraction_mode = not self.extraction_mode
        self.feature_detection_mode = False
        self.calibration_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.setCursor(QCursor(Qt.CrossCursor if self.extraction_mode else Qt.ArrowCursor))

        if self.extraction_mode:
            if self.image_processor.image is not None:
                print("Extraction mode enabled.")
                self.status_bar.showMessage("Extraction mode enabled.", 5000)
            else:
                print("Load an image first.")
                self.status_bar.showMessage("Load an image first.", 5000)
        else:
            print("Extraction mode disabled.")
            self.status_bar.showMessage("Extraction mode disabled.", 5000)
        self.image_view.selection_mode = not self.extraction_mode

        self.image_view.update_scene()
        self.image_view.update()

    def advanced_feature_detection(self):
        """Performs advanced feature detection on the image."""
        if self.image_processor.image is not None:
            print("Running advanced feature detection...")
            result_image = self.extraction.automatic_extraction(self.image_processor.image)
            self.image_view.set_image(result_image)
            self.status_bar.showMessage("Advanced feature detection completed.", 5000)
        else:
            print("Load an image first.")
            self.status_bar.showMessage("Load an image first.", 5000)

    def correct_perspective(self, points):
        """Corrects the perspective of the image using four points."""
        if len(points) != 4:
            return
        pts1 = np.float32([[point.x(), point.y()] for point in points])
        width, height = self.image_processor.image.shape[1], self.image_processor.image.shape[0]
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        self.image_processor.correct_perspective(pts1, pts2)
        self.update_image()
        self.image_view.clear_perspective_points()  # Clear the perspective points after correction
        self.status_bar.showMessage("Perspective corrected.", 5000)

    def toggle_feature_detection_mode(self):
        """Toggles the advanced feature detection mode."""
        if not self.calibration.calibration_done or len(self.calibration.calibration_points) < 4:
            QMessageBox.warning(self, "Calibration Required",
                                "Calibration is required before feature detection. Please calibrate at least 4 points.")
            return

        self.image_view.update_scene()
        self.feature_detection_mode = not self.feature_detection_mode
        self.calibration_mode = False
        self.extraction_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.setCursor(QCursor(Qt.CrossCursor if self.feature_detection_mode else Qt.ArrowCursor))

        if self.feature_detection_mode:
            if self.image_processor.image is not None:
                print("Running advanced feature detection...")
                result_image = self.extraction.automatic_extraction(self.image_processor.image)
                self.image_view.set_image(result_image)
                self.image_view.draw_detected_points(self.extraction.temp_points)
                self.status_bar.showMessage("Advanced feature detection enabled.", 5000)
            else:
                print("Load an image first.")
                self.status_bar.showMessage("Load an image first.", 5000)
        else:
            self.extraction.clear_temp_points()
            self.image_view.clear_detected_points()
            self.image_view.update_scene()
            self.interpolation.clear_interpolated_points()  # Ensure interpolated points are cleared
            self.status_bar.showMessage("Advanced feature detection disabled.", 5000)
        self.image_view.selection_mode = not self.feature_detection_mode
    def draw_confidence_intervals(self, x_new, lower_bound, upper_bound):
        """Draws confidence intervals for the interpolated points."""
        for x, y_low, y_high in zip(x_new, lower_bound, upper_bound):
            low_point = self.calibration.inverse_transform_point(x, y_low)
            high_point = self.calibration.inverse_transform_point(x, y_high)
            self.image_view.scene.addLine(low_point.x(), low_point.y(), high_point.x(), high_point.y(),
                                          QPen(Qt.red, 0.5))
    def show_error_metric(self, rmse):
        """Displays the RMSE of the interpolation."""
        QMessageBox.information(self, "Interpolation Error", f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    def toggle_perspective_mode(self):
        """Toggles the perspective correction mode."""
        self.image_view.update_scene()
        self.perspective_mode = not self.perspective_mode
        self.calibration_mode = False
        self.extraction_mode = False
        self.interpolation_mode = False
        self.feature_detection_mode = False
        self.setCursor(QCursor(Qt.CrossCursor if self.perspective_mode else Qt.ArrowCursor))
        self.update_perspective_info()
        self.image_view.selection_mode = not self.perspective_mode
        if not self.perspective_mode:
            self.image_view.clear_perspective_points()  # Clear the points if perspective mode is disabled
            self.status_bar.showMessage("Perspective mode disabled.", 5000)
        else:
            self.status_bar.showMessage("Perspective mode enabled.", 5000)

    def update_perspective_info(self):
        """Updates the informational label for perspective correction."""
        messages = [
            "Please select the top-left corner",
            "Please select the top-right corner",
            "Please select the bottom-left corner",
            "Please select the bottom-right corner"
        ]
        if self.perspective_mode and len(self.image_view.perspective_points) < 4:
            self.image_view.show_info_label(messages[len(self.image_view.perspective_points)])
        else:
            self.image_view.info_label.hide()

    def rotate_image(self):
        """Rotates the image by a specified angle."""
        angle, ok = QInputDialog.getDouble(self, "Rotate Image", "Enter angle (degrees) (clockwise):", 0, -360, 360, 1)
        if ok and self.image_processor.image is not None:
            self.image_processor.rotate_image(angle)
            self.update_image()
            self.status_bar.showMessage(f"Image rotated by {angle} degrees.", 5000)

    def update_image(self):
        """Updates the displayed image."""
        if self.image_processor.image is not None:
            self.image_view.set_image(self.image_processor.image)
            self.status_bar.showMessage("Image updated.", 5000)

    def equalize_histogram(self):
        """Equalizes the histogram of the image."""
        self.image_processor.equalize_histogram()
        self.update_image()
        self.status_bar.showMessage("Histogram equalized.", 5000)

    def edge_detection(self):
        """Applies edge detection to the image."""
        self.image_processor.edge_detection()
        self.update_image()
        self.status_bar.showMessage("Edge detection applied.", 5000)

    def denoise_image(self):
        """Applies denoising to the image."""
        self.image_processor.denoise_image()
        self.update_image()
        self.status_bar.showMessage("Image denoised.", 5000)
    def toggle_calibration_mode(self):
        """Toggles the calibration mode."""
        self.calibration_mode = not self.calibration_mode
        self.extraction_mode = False
        self.interpolation_mode = False
        self.perspective_mode = False
        self.feature_detection_mode = False
        self.setCursor(QCursor(Qt.CrossCursor if self.calibration_mode else Qt.ArrowCursor))
        self.image_view.selection_mode = not self.calibration_mode
        if self.calibration_mode:
            self.status_bar.showMessage("Calibration mode enabled.", 5000)
        else:
            self.status_bar.showMessage("Calibration mode disabled.", 5000)

    def toggle_interpolation_mode(self):
        """Toggles the interpolation mode."""
        if not self.calibration.calibration_done or len(self.calibration.calibration_points) < 4:
            QMessageBox.warning(self, "Calibration Required",
                                "Calibration is required before interpolation. Please calibrate at least 4 points.")
            return
        self.interpolation_mode = not self.interpolation_mode
        self.calibration_mode = False
        self.extraction_mode = False
        self.feature_detection_mode = False
        self.perspective_mode = False

        if self.interpolation_mode:
            if len(self.extraction.data_points) >= 2:
                self.interpolation.calibration = self.calibration
                print("Interpolation mode activated.")
                print("Data points:", self.extraction.get_data_points())
                if self.interpolation.method == 'linear':
                    interpolated_points = self.interpolation.interpolate_data(self.extraction.get_data_points())
                    self.image_view.draw_interpolated_points(interpolated_points)
                elif self.interpolation.method == 'spline':
                    interpolated_points, x_new, lower_bound, upper_bound = self.interpolation.interpolate_data(self.extraction.get_data_points())
                    self.image_view.draw_interpolated_points(interpolated_points)
                    self.image_view.draw_confidence_intervals(x_new, lower_bound, upper_bound)
                elif self.interpolation.method in ['polynomial', 'akima', 'pchip', 'quadratic', 'piecewise_linear']:
                    interpolated_points = self.interpolation.interpolate_data(self.extraction.get_data_points())
                    self.image_view.draw_interpolated_points(interpolated_points)
                self.show_data_points()
                self.update_image()
                self.status_bar.showMessage("Interpolation mode enabled.", 5000)
            else:
                QMessageBox.warning(self, "Insufficient Data Points",
                                    "At least 2 data points are required for interpolation.")
                self.interpolation_mode = False
        else:
            self.interpolation.clear_interpolated_points()
            self.status_bar.showMessage("Interpolation mode disabled.", 5000)
        self.image_view.selection_mode = not self.interpolation_mode

    def export_data_as_csv(self):
        """Exports the data points as a CSV file."""
        if not self.calibration.calibration_done or len(self.calibration.calibration_points) < 4:
            QMessageBox.warning(self, "Calibration Required",
                                "Calibration is required before exporting data points. Please calibrate at least 4 points.")
            return

        if self.interpolation_mode:
            real_coordinates = [point.get_real_coordinates() for point in self.interpolation.interpolated_points]
        else:
            real_coordinates = [point.get_real_coordinates() for point in self.extraction.data_points]

        if real_coordinates:
            options = QFileDialog.Options()
            filepath, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv);;All Files (*)",
                                                      options=options)
            if filepath:
                self.data_exporter.export_to_csv(real_coordinates, filepath)
                self.status_bar.showMessage(f"Data exported as CSV to {filepath}.", 5000)
    def export_data_as_json(self):
        """Exports the data points as a JSON file."""
        if not self.calibration.calibration_done or len(self.calibration.calibration_points) < 4:
            QMessageBox.warning(self, "Calibration Required",
                                "Calibration is required before exporting data points. Please calibrate at least 4 points.")
            return

        if self.interpolation_mode:
            real_coordinates = [point.get_real_coordinates() for point in self.interpolation.interpolated_points]
        else:
            real_coordinates = [point.get_real_coordinates() for point in self.extraction.data_points]

        if real_coordinates:
            options = QFileDialog.Options()
            filepath, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json);;All Files (*)",
                                                      options=options)
            if filepath:
                self.data_exporter.export_to_json(real_coordinates, filepath)
                self.status_bar.showMessage(f"Data exported as JSON to {filepath}.", 5000)

    # Automatic calibration handler in main_window.py
    def automatic_calibration(self):
        """Performs automatic calibration of the image."""
        if self.image_processor.image is not None:
            print("Running automatic calibration...")
            self.calibration.automatic_calibration(self.image_processor.image)
            self.status_bar.showMessage("Automatic calibration completed.", 5000)
        else:
            print("Load an image first.")
            self.status_bar.showMessage("Load an image first.", 5000)

    def show_data_points(self):
        """Displays the list of data points."""
        self.data_points_list.clear()
        data_points = self.extraction.get_data_points()
        interpolated_points = self.interpolation.interpolated_points if self.interpolation_mode else []

        for i, point in enumerate(data_points):
            real_coords = point.get_real_coordinates()
            if real_coords is not None:
                coord_str = f"({real_coords.x():.2f}, {real_coords.y():.2f})"
            else:
                coord_str = "(None)"
            item = QListWidgetItem(f"Data Point {i + 1}: {coord_str}")
            item.setData(Qt.UserRole, point)  # Store the Point instance
            self.data_points_list.addItem(item)

        for i, point in enumerate(interpolated_points):
            real_coords = point.get_real_coordinates()
            if real_coords is not None:
                coord_str = f"({real_coords.x():.2f}, {real_coords.y():.2f})"
            else:
                coord_str = "(None)"
            item = QListWidgetItem(f"Interpolated Point {i + 1}: {coord_str}")
            item.setData(Qt.UserRole, point)  # Store the Point instance
            self.data_points_list.addItem(item)
    def edit_data_point(self, item):
        """Edits the selected data point."""

        if isinstance(item, QGraphicsEllipseItem):
            point = item.data(0)  #
            real_coords = point.get_real_coordinates()
            x, ok_x = QInputDialog.getDouble(self, "Edit Point", "X Coordinate:", real_coords.x(), -10000, 10000, 2)
            y, ok_y = QInputDialog.getDouble(self, "Edit Point", "Y Coordinate:", real_coords.y(), -10000, 10000, 2)
            if ok_x and ok_y:
                # Update real coordinates
                new_real_coords = QPointF(x, y)
                # Convert new real coordinates to image coordinates
                new_image_coords = self.calibration.inverse_transform_point(x, y)
                point.set_image_coordinates(new_image_coords)
                point.set_real_coordinates(new_real_coords)
                self.image_view.update_scene()
                self.show_data_points()
                self.save_undo_state("edit_data_point", item, point)
                self.status_bar.showMessage("Data point edited.", 5000)
            else:
                QMessageBox.warning(self, "Invalid Selection", "Cannot edit an interpolated point.")
        else:
            point = item.data(Qt.UserRole)
            real_coords = point.get_real_coordinates()
            x, ok_x = QInputDialog.getDouble(self, "Edit Point", "X Coordinate:", real_coords.x(), -10000, 10000, 2)
            y, ok_y = QInputDialog.getDouble(self, "Edit Point", "Y Coordinate:", real_coords.y(), -10000, 10000, 2)

            if ok_x and ok_y:
                # Update real coordinates
                new_real_coords = QPointF(x, y)
                # Convert new real coordinates to image coordinates
                new_image_coords = self.calibration.inverse_transform_point(x, y)
                point.set_image_coordinates(new_image_coords)
                point.set_real_coordinates(new_real_coords)
                self.image_view.update_scene()
                self.show_data_points()
                self.save_undo_state("edit_data_point", item, point)
                self.status_bar.showMessage("Data point edited.", 5000)
            else:
                QMessageBox.warning(self, "Invalid Selection", "Cannot edit an interpolated point.")
    def delete_data_point(self, item=None):
        """Deletes a selected data point or multiple selected data points."""
        if item:
            point = item.data(0)
            if point in self.extraction.data_points:
                self.extraction.data_points.remove(point)
            elif point in self.interpolation.interpolated_points:
                self.interpolation.interpolated_points.remove(point)
            self.image_view.delete_highlight(point)
        else:
            items = self.image_view.selected_items
            for item in items:
                point = item.data(0)
                if point in self.extraction.data_points:
                    self.extraction.data_points.remove(point)
                elif point in self.interpolation.interpolated_points:
                    self.interpolation.interpolated_points.remove(point)
                self.image_view.delete_highlight(point)
        self.image_view.clear_selection()
        self.show_data_points()
        self.update_image()
        self.status_bar.showMessage("Data point(s) deleted.", 5000)



    def open_plot_window(self):
        data_points = self.extraction.get_data_points()
        interpolated_points = self.interpolation.interpolated_points if self.interpolation_mode else None
        self.plot_window = PlotWindow(data_points, interpolated_points, self)
        self.plot_window.show()

    def save_undo_state(self, action, item, point):
        """Saves the current state for undo functionality."""
        self.undo_stack.append((action, item, point))
        self.redo_stack.clear()
        self.status_bar.showMessage("Undo state saved.", 5000)
    def reset_view(self):
        """Resets the view by centering and resetting zoom."""
        self.image_view.reset_view()

    def undo(self):
        """Undo the last action."""
        if not self.undo_stack:
            return
        action, item, point = self.undo_stack.pop()
        if action == "edit_data_point":
            self.redo_stack.append((action, item, point))
            self.edit_data_point(item)
        elif action == "delete_data_point":
            self.redo_stack.append((action, item, point))
            self.extraction.data_points.append(point)
            self.show_data_points()
            self.update_image()

    def redo(self):
        """Redo the last undone action."""
        if not self.redo_stack:
            return
        action, item, point = self.redo_stack.pop()
        if action == "edit_data_point":
            self.undo_stack.append((action, item, point))
            self.edit_data_point(item)
        elif action == "delete_data_point":
            self.undo_stack.append((action, item, point))
            self.extraction.data_points.remove(point)
            self.show_data_points()
            self.update_image()

    def reset_application(self):
        """Resets the application to its initial state."""
        # Clear calibration points
        self.calibration.clear_calibration_points()

        # Clear data points
        self.extraction.data_points = []


        #temporary points
        self.extraction.clear_temp_points()
        self.image_view.clear_detected_points()

        #interpolate points
        self.interpolation.clear_interpolated_points()

        #image
        self.image_processor.image = None


        # Reset UI
        self.status_bar.clearMessage()
        self.setCursor(QCursor(Qt.ArrowCursor))

        # Disable actions
        self.calibrationAction.setEnabled(False)
        self.automaticCalibrationAction.setEnabled(False)
        self.extractionAction.setEnabled(False)
        self.histogramAction.setEnabled(False)
        self.edgeAction.setEnabled(False)
        self.denoiseAction.setEnabled(False)
        self.perspectiveAction.setEnabled(False)
        self.rotateAction.setEnabled(False)
        self.detectedPointsAction.setEnabled(False)

        self.status_bar.showMessage("Application reset to initial state.", 5000)