from pathlib import Path
import os
import sys

user_home_dir = Path.home()


# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
# https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables
# https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/MacOSXDirectories/MacOSXDirectories.html
def get_os_user_data_dir() -> Path:
    if os.name == "posix":
        if sys.platform.startswith("darwin"):
            return Path("~/Library/Application Support").expanduser()

        return Path(
            os.environ.get("XDG_DATA_HOME", "~/.local/share")
        ).expanduser()
    if os.name == "nt":
        return Path(os.environ["APPDATA"])

    raise RuntimeError(
        f"Can't get user data directory on platform {os.name} {sys.platform}"
    )


def get_app_data_dir() -> Path:
    return get_os_user_data_dir() / "pymetheus"


def get_default_lib_filename() -> str:
    return "pymetheus.sqlite"


def get_default_library_path() -> Path:
    return get_app_data_dir() / get_default_lib_filename()


def search_library_file_with_precedence(
        order: list[Path],
        /,
) -> Path | None:
    for specified_path in order:
        found_lib = search_library_file(specified_path)
        if found_lib:
            return found_lib

    # No library found in the specified paths, search their parents now
    for specified_path in order:
        for parent in specified_path.parents:
            found_lib = search_library_file(parent)
            if found_lib:
                return found_lib

    # Sorry, no library found.
    return None


def search_library_file(path: Path, /) -> Path | None:
    path = path.expanduser().resolve()
    if path.is_dir():
        lib_path = path / get_default_lib_filename()
        if lib_path.is_file():
            return lib_path
        return None

    if path.is_file():
        return path

    return None
