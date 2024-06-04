import customtkinter
from customtkinter import filedialog
from tksheet import Sheet
import json
import sqlite3
import os
import pandas as pd
from time import sleep
from threading import Thread
from sql_formatter.core import format_sql
from packages.events.syntax_events import SytanxErrorHandler
from packages.events.syntax_events import TextColoringHandler
from packages.events import SQLEventHandler
from packages.events.syntax_events import FormatTextHandler
from packages.utils import strip_triple

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    """
    Custom Application Class
    ------------------------

    This class represents the main application window and its functionalities.


    """

    def __init__(self):
        """
        Constructor method of the class.
        """
        super().__init__()

        self._syntax_error_handler: SytanxErrorHandler = SytanxErrorHandler(self)
        self._text_coloring_handler: TextColoringHandler = TextColoringHandler(self)
        self._main_connection: sqlite3.Connection = None
        self._main_cursor: sqlite3.Cursor = None
        self._format_event: FormatTextHandler = None
        self._file_path: str = ""

        self.bind("<Control-z>", self.get_older_query)
        self.bind("<Control-Shift-Z>", self.get_new_old_query)

        # configure window
        self.title("")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.attributes("-fullscreen", True)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((1, 1, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="TableTracker",
            font=customtkinter.CTkFont(family="Courier", size=20, weight="bold"),
        )
        self.quick_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="QuickTable",
            font=customtkinter.CTkFont(family="Courier", size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.quick_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Close Connection",
            command=self.close_connection,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Formatting",
            command=self.format_sql_query,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Save Query",
            command=self.save_query,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Open File",
            command=self.get_info_from_file,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_5.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Save Data as Json",
            command=self.save_json,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_6.grid(row=7, column=0, padx=20, pady=10)
        self.sidebar_button_7 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Save Data as Csv",
            command=self.save_csv,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_7.grid(row=8, column=0, padx=20, pady=10)
        self.sidebar_button_8 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Exit",
            command=exit,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.sidebar_button_8.grid(row=9, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Appearance Mode:",
            anchor="w",
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.appearance_mode_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 0))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="UI Scaling:",
            anchor="w",
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.scaling_label.grid(row=13, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.scaling_optionemenu.grid(row=14, column=0, padx=20, pady=(10, 0))

        self.syntax_error_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Syntax Error",
            anchor="w",
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.syntax_error_label.grid(row=15, column=0, padx=20, pady=(10, 0))

        self.syntax_error_optionmenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["On", "Off"],
            command=self._syntax_error_handler.change_syntax_on_off,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.syntax_error_optionmenu.grid(row=16, column=0, padx=20, pady=(10, 20))

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            text="Execute",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.create_sql_event,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.main_button_1.grid(
            row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.sheet: Sheet = Sheet(
            self,
            theme="light green",
            height=(self.winfo_screenheight() // 2 + self.winfo_screenheight() // 5),
            data=[[]],
            headers=[],
            font=("Courier", 13, "normal"),
        )
        self.sheet.grid(
            sticky="nsew",
            row=2,
            rowspan=2,
            column=1,
            columnspan=3,
            padx=(0, 20),
            pady=(20, 0),
        )
        # create textbox
        self.textbox = customtkinter.CTkTextbox(
            self,
            width=425,
            wrap="word",
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.textbox.bind("<Enter>", self._analyze_text)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="new")

        self.output_frame = customtkinter.CTkScrollableFrame(
            self, width=425, orientation=("horizontal", "vertical")
        )
        self.output_label = customtkinter.CTkLabel(
            self.output_frame,
            width=400,
            font=customtkinter.CTkFont(family="Courier"),
            text="Output Window",
        )
        self.output_label.grid(column=0, row=0, sticky="nsew")
        self.output_frame.grid(
            row=1,
            column=2,
            columnspan=2,
            padx=(20, 20),
            pady=(20, 0),
            sticky="new",
        )

        self.enter_db = customtkinter.CTkEntry(
            self,
            placeholder_text="Create or Enter DB",
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.enter_db.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.enter_db_button = customtkinter.CTkButton(
            master=self,
            text="Create or Enter DB",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self._connect_db,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.enter_db_button.grid(
            row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )

        self.select_page_menu = customtkinter.CTkOptionMenu(
            master=self,
            values=["Page 1"],
            command=self.change_output_page,
            font=customtkinter.CTkFont(family="Courier"),
        )
        self.select_page_menu.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.syntax_error_optionmenu.set("On")
        self.textbox.insert("0.0", "Enter SQL Lite Queries Here")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Change appearance mode event handler.

        :param new_appearance_mode: New appearance mode.
        :type new_appearance_mode: str
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str) -> None:
        """
        Change the scaling of the widgets.

        :param new_scaling: New scaling value as a percentage string.
        :type new_scaling: str
        :return: None
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_output_page(self, page_name: str) -> None:
        """
        Change the output page.
        :param page_name: Name of the page to change to.
        :type page_name: String
        :return: None
        """

        if self._format_event is not None:
            self._format_event.handle(page_name)

    def save_csv(self) -> None:
        """
        Save the data as a CSV file.
        :return: None
        """
        thread: Thread = Thread(target=self._save_csv, daemon=True)
        thread.start()

    def _save_csv(self) -> None:
        """
        Save the data as a CSV file.
        This method saves the data as a CSV file. It first converts the data to a DataFrame,
        then saves it as a CSV file, and finally removes the temporary JSON file.

        :return: None
        """
        try:
            file_name_list: list = self._file_path.split("/")
            file_name_list[-1] = "tmp_" + file_name_list[-1]
            file_name: str = "".join(file_name_list)
            self._save_json(file_name=f"{file_name}")
            df: pd.DataFrame = pd.read_json(f"{file_name}.json")
            df.to_csv(f"{self._file_path}.csv")
            os.remove(f"{file_name}.json")
            self.set_result_label = f"{self._file_path}.csv has been saved"
        except BaseException:
            self.set_result_label = f"{self._file_path}.csv has not been saved"

    def save_json(self) -> None:
        """
         Save the data as a JSON file.
        :return: None
        """
        thread: Thread = Thread(target=self._save_json, daemon=True)
        thread.start()

    def _save_json(self, file_name: str = False):
        """Perform the actual saving of data as a JSON file.

        This method collects data from the sheet and saves it as a JSON file. If no file name is provided,
        it uses the default file path.

        :param file_name: Optional. The name of the JSON file to be saved.
        :type file_name: str
        """
        try:
            file_name = file_name or self._file_path
            json_dict: dict = {}
            for i in range(1, 999):
                try:
                    if not bool(self.sheet.get_header_data(c=i)):
                        raise AttributeError
                    json_dict.update(
                        {
                            self.sheet.get_header_data(c=i): self.sheet.get_column_data(
                                c=i
                            )
                        }
                    )
                except BaseException:
                    break
            with open(f"{file_name}.json", "w") as f:
                f.write(json.dumps(json_dict, indent="\t"))
            self.set_result_label = f"{file_name}.json has been saved"
        except BaseException:
            self.set_result_label = f"{self._file_path}.csv has not been saved"

    @staticmethod
    def _current_saved_query(files: list[str]) -> int:
        """
        Get the number of currently saved query files.
        :param files: List of file names in the current directory.
        :type files: list[str]
        :return: Number of currently saved query files.
        :rtype: int
        """
        current_query_file: int = 0
        for file_name in files:
            if file_name.startswith("query"):
                current_query_file += 1
        return current_query_file

    def save_query(self):
        """
         Save the SQL query as a file.

        This method initiates the process of saving the current SQL query as a file. It starts a new thread
        to handle the saving operation asynchronously.


        """

        thread: Thread = Thread(target=self._save_query, daemon=True)
        thread.start()

    def _save_query(self):
        """
        Save the SQL query as a file.

        This method performs the actual saving of the SQL query as a file. It checks if the query is complete,
        retrieves the list of files in the current directory, calculates the number of currently saved query
        files, and then saves the query text to a new file with a name based on the count of saved queries.


        """

        try:
            if sqlite3.complete_statement(self.get_textbox_text):
                files: list[str] = os.listdir(".")
                current_query_file: int = self._current_saved_query(files)
                with open(f"query-{current_query_file}.sql", "w") as f:
                    self.format_sql_query()
                    f.writelines(self.get_textbox_text)
                    self.set_result_label = (
                        f"Query saved as query-{current_query_file}.sql to ./"
                    )
            else:
                self.set_result_label = "Complete the query"
        except BaseException:
            self.set_result_label = f"{current_query_file}.sql has not been saved"

    def get_older_query(self, event):
        """
         Retrieve the older query.
         This method retrieves the older query from the history of executed queries. It updates the textbox
         with the previous query text and decrements the query index. If there are no more older queries,
         it displays a message indicating that the bottom of the query history has been reached.

        :param event: Event object triggering the method.

        """
        if SQLEventHandler.query_index > 0:
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert(
                "0.0", SQLEventHandler.queries[SQLEventHandler.query_index]
            )
            SQLEventHandler.query_index -= 1
            self._add_final_space()
            self._text_coloring_handler.handle()
        else:
            self.set_result_label = "You have reached the bottom query"

    def get_new_old_query(self, event):
        """
        Get the next query from the history.
        :param event: Event object triggering the method.
        """

        if SQLEventHandler.query_index <= len(SQLEventHandler.queries) - 2:
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert(
                "0.0", SQLEventHandler.queries[SQLEventHandler.query_index]
            )
            SQLEventHandler.query_index += 1
            self._add_final_space()
            self._text_coloring_handler.handle()
        else:
            self.set_result_label = "You have reached the top query"

    def get_info_from_file(self):
        """
        Get information from selected file(s).
        """
        files: str = filedialog.askopenfilenames(defaultextension=".")
        if not bool(files):
            self.set_result_label = "As First Drop One File"
            return
        for current_file in files:
            thread: Thread = Thread(
                target=self.file_action, args=(current_file,), daemon=True
            )
            thread.start()

    def file_action(self, file_name: str):
        """
         Perform action based on the file type.
        :param file_name: Name of the file to process.
        : type file_name: str
        """
        if file_name[-4:] != ".sql" and file_name[-3:] != ".db":
            self.set_result_label = "Only .db or .sql path"
            self._delete_files([self._get_correct_path(file_name)])
            return None
        elif file_name[-4:] == ".sql":
            with open(file_name, "r") as f:
                self.textbox.delete("0.0", customtkinter.END)
                self.textbox.insert("0.0", strip_triple("".join(f.readlines())))
                self._add_final_space()
                self._text_coloring_handler.handle()
            return None
        else:
            if self._main_connection is not None:
                self.close_connection()
            self._connect_db(file_name=file_name)
            return None

    def _get_correct_path(self, file_path: str):
        """
        Adjusts file path according to OS

        :param file_path: file path
        :type file_path: str

        :return : file path of temporary file
        :rtype:str
        """
        if sys.platform == "linux":
            deletation_file: str = self.get_dropfile_tempdir() + "/" + file_path
        elif sys.platform == "win32":
            deletation_file: str = self.get_dropfile_tempdir() + "\\" + file_path
        return deletation_file

    @staticmethod
    def _delete_files(file_paths: list[str], *, sleeping: bool = False):
        """
        Deletes temporary files

        :param file_paths: A list of file paths to delete.
        :type file_paths: list[str]
        :param sleeping: Whether to sleep between deletion attempts. Defaults to False.
        :type sleeping: bool
        :return: None
        """
        deleted: bool = True
        while deleted:
            try:
                for _ in map(os.remove, file_paths):
                    continue
                deleted = False
            except (OSError, EOFError):
                if sleeping:
                    sleep(0.5)
        return None

    def format_sql_query(self) -> None:
        thread: Thread = Thread(target=self._format_sql_query, daemon=True)
        thread.start()

    def _format_sql_query(self):
        """
        Format SQL query.

        This method is called in a separate thread to format the SQL query present in the textbox.
        """
        formatted_sql: str = format_sql(self.get_textbox_text, max_len=1000000000)
        self.textbox.delete("1.0", customtkinter.END)
        self.textbox.insert("1.0", formatted_sql)
        self._add_final_space()
        self._text_coloring_handler.handle()

    def get_table_names(self) -> None:
        """
        Get table names.

        This method retrieves the table names from the connected database and displays them.
        :return : None
        """

        if self._main_connection is not None:
            query: str = (
                f"""SELECT name FROM sqlite_master WHERE type='table'; /* {self.get_db_name} */"""
            )
            event: SQLEventHandler = SQLEventHandler(
                query, self._main_cursor, self.output_label
            )
            self.format_event: FormatTextHandler = FormatTextHandler(self, event)
            self.format_event.handle()
            self._main_connection.commit()
        else:
            self.set_result_label = "As first connect db"

    def close_connection(self) -> None:
        """
        Close database connection.

        This method closes the connection to the database, if one exists, and sets a corresponding label.
        return: None
        """
        if self._main_connection is not None:
            self._main_connection.close()
        self.set_result_label = "Connection closed"

    @property
    def get_textbox_text(self) -> str:
        """
        Get text from the textbox.

        :return: Text content of the textbox.
        :rtype: str
        """
        return strip_triple(self.textbox.get("1.0", "end"))

    def _add_page(self, *args):
        """
        Add pages to the select page menu.

        :param args: Page values.
        :raises TypeError: If any of the page values are not of type str.
        """
        if any([type(arg) is not str for arg in args]):
            raise TypeError("Page values are not str")
        self.select_page_menu.configure(values=args)

    @property
    def get_db_name(self) -> str:
        """
        Get the database name from the input field.

        :return: Database name.
        :rtype: str
        """
        return strip_triple(self.enter_db.get())

    @property
    def _output_label(self) -> customtkinter.CTkLabel:
        """
        Get the output label.

        :return: Output label.
        :rtype: customtkinter.CTkLabel
        """
        return self.output_label

    @_output_label.setter
    def set_result_label(self, text: str) -> None:
        """
        Set text for the result label.

        :param text: Text to set.
        :type text: str
        return: None
        """
        self.output_label.configure(text=strip_triple(text))

    def _check_db_file_ishere(self) -> bool:
        """
        Check if the database file is present.

        :return: True if the file is present, False otherwise.
        :rtype: bool
        """
        if self.get_db_name not in set(os.listdir(".")):

            self.set_result_label = (
                f"There is no such db named {self.get_db_name}\n"
                + f"You have created db named {self.get_db_name}"
            )
            return False
        return True

    def _connect_db(self, file_name: str = "") -> None:
        """
        Connect to the database.

        :param file_name: Name of the file.
        :type file_name: str
        :return: None
        """
        file_name = self.get_db_name or file_name
        self._file_path = file_name
        if ".db" == file_name[-3:]:
            self._check_db_file_ishere()
            try:
                self._file_path = file_name
                self.set_result_label = "Connected to db"
            except sqlite3.Error:
                print("connect_db error")
                self.set_result_label = f"There is no such db named {file_name}"

        else:
            self.set_result_label = f"Wrong db name : {file_name}"

    def create_sql_event(self) -> None:
        """
        Create SQL event.
        :return: None
        """
        thread: Thread = Thread(target=self._create_sql_event, daemon=True)
        thread.start()

    def _create_sql_event(self):
        """
        Implementation of creating SQL event.
        """
        if self._main_connection is not None:
            sleep(0.2)
        if not sqlite3.complete_statement(self.get_textbox_text):
            self.set_result_label = (
                f"{self.get_textbox_text}\n\n\n\nThis query is not complete"
            )
            return
        self._main_connection = sqlite3.connect(self._file_path)
        event: SQLEventHandler = SQLEventHandler(
            self.get_textbox_text, self._main_connection.cursor(), self.output_label
        )
        self.format_event: FormatTextHandler = FormatTextHandler(self, event)
        self.format_event.handle()
        self._main_connection.commit()
        self._main_connection.close()
        self._main_connection = None

    def _add_final_space(self) -> None:
        """
        Add a final space to the text in the textbox.
        :return: None
        """
        textbox_text: str = self.get_textbox_text
        self.textbox.delete("1.0", customtkinter.END)
        textbox_text += " "
        self.textbox.insert("1.0", textbox_text)

    def _analyze_text(self, event) -> None:
        """
        Analyze text event handler.

        :param event: Event object.

        :return:None
        """

        self._text_coloring_handler.handle()
        self._syntax_error_handler.handle()


if __name__ == "__main__":

    app = App()
    app.mainloop()
