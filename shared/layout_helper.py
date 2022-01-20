try:
    from typing import List
except ImportError:
    pass

# cribbed from adafruit_display_notification
def wrap_text(string: str, max_chars: int) -> List[str]:
    """A helper that will return a list of lines with word-break wrapping.

    :param str string: The text to be wrapped.
    :param int max_chars: The maximum number of characters on a line before wrapping.
    """

    string = string.replace("\n", "").replace("\r", "")  # strip confusing newlines
    words = string.split(" ")
    the_lines = []
    the_line = ""
    for w in words:
        if len(the_line + " " + w) <= max_chars:
            the_line += " " + w
        else:
            the_lines.append(the_line)
            the_line = "" + w
    if the_line:  # last line remaining
        the_lines.append(the_line)
    # remove first space from first line:
    the_lines[0] = the_lines[0][1:]
    return the_lines
