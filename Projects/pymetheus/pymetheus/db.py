import argparse
import os
import sqlite3
from pathlib import Path

from .paths import (
    search_library_file_with_precedence,
    get_app_data_dir,
    get_default_library_path
)


def create_library_at(path: Path, /) -> sqlite3.Connection:
    path.parent.mkdir(exist_ok=True, parents=True)
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    current_path = Path(__file__).resolve()
    ddl_path = current_path.parent / "ddl" / "main.sql"

    cursor.executescript(ddl_path.read_text("utf-8"))
    connection.commit()
    return connection


def open_library_at(path: Path, /) -> sqlite3.Connection:
    if path.exists():
        return sqlite3.connect(path)
    return create_library_at(path)


def get_connection_from_args(
        parsed_args: argparse.Namespace,
        /
) -> tuple[Path, sqlite3.Connection]:
    if not parsed_args.library:
        library_path = search_library_file_with_precedence(
            [
                Path(os.getcwd()),
                get_app_data_dir(),
            ]
        )
        if not library_path:
            library_path = get_default_library_path()
            return library_path, create_library_at(library_path)
        else:
            return library_path, open_library_at(library_path)
    else:
        library_path: Path = parsed_args.library
        if library_path.exists():
            return library_path, open_library_at(library_path)
        else:
            return library_path, create_library_at(library_path)
