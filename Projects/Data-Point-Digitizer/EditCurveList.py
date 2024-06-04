import tkinter as tk


class EditCurveList:
    def __init__(self, viewer):
        """
        Initialize the EditCurveList class.

        Parameters:
        viewer (Viewer): An instance of a viewer class that provides data.
        """
        self.viewer = viewer
        self.list_window = None

    def open_list_window(self):
        """
        Open a new window to display and edit the list of curves.
        If a list window is already open, it will be destroyed and recreated.
        """
        if self.list_window is not None:
            self.list_window.destroy()

        self.list_window = tk.Toplevel(self.viewer.root)
        self.list_window.title("Curve List")

        listbox = tk.Listbox(self.list_window, selectmode=tk.SINGLE)
        for curve in self.viewer.curve_IDs:
            listbox.insert(tk.END, self.viewer.curve_names[curve - 1])
        listbox.pack()

        change_button = tk.Button(
            self.list_window,
            text="Change Curve Name",
            command=lambda: self.change_curve_name(listbox.get(listbox.curselection()))
        )
        change_button.pack()

    def change_curve_name(self, curve_name):
        """
        Open a window to change the name of the selected curve.

        Parameters:
        curve_name (str): The name of the curve to be changed.
        """
        entry_window = tk.Toplevel(self.list_window)
        entry_window.title("Change Curve Name")

        tk.Label(entry_window, text="Enter new curve name:").pack()
        entry = tk.Entry(entry_window)
        entry.pack()

        def save_new_name():
            new_name = entry.get()
            if new_name:
                index = self.viewer.curve_names.index(curve_name)
                self.viewer.curve_names[index] = new_name
                self.open_list_window()
            entry_window.destroy()

        save_button = tk.Button(entry_window, text="Save", command=save_new_name)
        save_button.pack()
