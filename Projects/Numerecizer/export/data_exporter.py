import csv
import json
from PyQt5.QtCore import QPointF

class DataExporter:
    """Class to handle exporting data points to CSV and JSON formats."""

    def export_to_csv(self, data_points, filepath):
        """Exports data points to a CSV file."""
        try:
            with open(filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])
                for point in data_points:
                    if isinstance(point, QPointF):
                        writer.writerow([point.x(), point.y()])
                    else:
                        writer.writerow([None, None])
            print(f"Data successfully exported to {filepath}")
        except Exception as e:
            print(f"Failed to export data to CSV: {e}")

    def export_to_json(self, data_points, filepath):
        """Exports data points to a JSON file."""
        data = [{"x": point.x(), "y": point.y()} for point in data_points if isinstance(point, QPointF)]
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Data successfully exported to {filepath}")
        except Exception as e:
            print(f"Failed to export data to JSON: {e}")
