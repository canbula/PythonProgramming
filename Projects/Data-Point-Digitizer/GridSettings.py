import tkinter as tk


class GridSettings:
    def __init__(self, parent):
        """
        Initialize the GridSettings class.

        Parameters:
        parent (tk.Widget): The parent widget that contains the settings.
        """
        self.parent = parent
        self.settings_window = None

    def open_settings_window(self):
        """
        Open a new window for grid settings. If a settings window is already open, it will be destroyed and recreated.
        """
        if self.settings_window is not None:
            self.settings_window.destroy()

        self.settings_window = tk.Toplevel(self.parent.root)
        self.settings_window.title("Grid Settings")

        # Label and scale for grid size X
        size_label_x = tk.Label(self.settings_window, text="Set Grid Size X:")
        size_label_x.grid(row=1, column=0, padx=5, pady=5)
        size_scale_x = tk.Scale(self.settings_window, from_=1, to=25, orient=tk.HORIZONTAL, command=self.change_size_x)
        size_scale_x.set(self.parent.grid_size_x)
        size_scale_x.grid(row=1, column=1, padx=5, pady=5)

        # Label and scale for grid size Y
        size_label_y = tk.Label(self.settings_window, text="Set Grid Size Y:")
        size_label_y.grid(row=2, column=0, padx=5, pady=5)
        size_scale_y = tk.Scale(self.settings_window, from_=1, to=25, orient=tk.HORIZONTAL, command=self.change_size_y)
        size_scale_y.set(self.parent.grid_size_y)
        size_scale_y.grid(row=2, column=1, padx=5, pady=5)

        # Button to apply settings
        apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_settings)
        apply_button.grid(row=3, column=0, columnspan=2, pady=10)

    def change_size_x(self, value):
        """
        Change the grid size in the X direction.

        Parameters:
        value (int): The new size value for the X axis.
        """
        self.parent.grid_size_x = value
        self.parent.draw_grid()

    def change_size_y(self, value):
        """
        Change the grid size in the Y direction.

        Parameters:
        value (int): The new size value for the Y axis.
        """
        self.parent.grid_size_y = value
        self.parent.draw_grid()

    def apply_settings(self):
        """
        Apply the selected settings and redraw the grid. Closes the settings window.
        """
        self.parent.draw_grid()
        self.settings_window.destroy()
