"""Shared helpers for reading and writing the fixed-width file formats.

Every system file uses fixed-width fields, so these helpers keep the
padding, trimming and number rules in one place instead of copying them
into each file class.
"""

from error_log import FatalFileError

# Field widths shared by every file format.
USERNAME_WIDTH = 15
GAME_NAME_WIDTH = 25
USER_TYPE_WIDTH = 2
CREDIT_WIDTH = 9
PRICE_WIDTH = 6

# Every system file ends with a line that starts with this marker.
END_MARKER = "END"


def read_field(line, start, width):
    """Return the text in line[start:start+width] with spaces trimmed."""
    return line[start:start + width].strip()


def read_money(line, start, width, file_name):
    """Return the number in a fixed-width money field, or raise
    FatalFileError if the field is not a valid number."""
    text = read_field(line, start, width)
    try:
        return float(text)
    except ValueError:
        raise FatalFileError(f"{file_name}: '{text}' is not a valid amount")


def pad_text(text, width):
    """Left-align text and pad it with spaces to exactly width characters."""
    return text.ljust(width)


def format_money(amount, width):
    """Format amount with two decimals, zero-padded to width (e.g. 001000.00)."""
    return f"{amount:0{width}.2f}"


def is_end_line(line, name_width):
    """Return True if the first field of line is the END marker."""
    return read_field(line, 0, name_width) == END_MARKER


def read_lines(path, file_name):
    """Return every line of the file at path (without newlines), or raise
    FatalFileError if the file can't be opened."""
    try:
        with open(path, "r") as input_file:
            return input_file.read().splitlines()
    except OSError:
        raise FatalFileError(f"{file_name}: unable to open '{path}'")


def write_lines(path, lines):
    """Write each line to the file at path, one per line."""
    with open(path, "w") as output_file:
        for line in lines:
            output_file.write(line + "\n")
