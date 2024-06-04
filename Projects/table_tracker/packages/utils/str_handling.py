def strip_triple(text: str) -> str:
    """
    Strips leading and trailing whitespace, tab characters, and newline characters from the given text.

    :param text: The text to be stripped.
    :type text: str
    :return: The stripped text.
    :rtype: str
    """
    stripped_text: str = text.strip().strip("\t").strip("\n")
    stripped_text: str = text.strip().strip("\n").strip("\t")
    stripped_text: str = text.strip("\t").strip().strip("\n")
    stripped_text: str = text.strip("\t").strip("\n").strip()
    stripped_text: str = text.strip("\n").strip("\t").strip()
    stripped_text: str = text.strip("\n").strip().strip("\t")
    return stripped_text
