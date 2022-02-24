import sys
import re

try:
    import typing  # pylint: disable=unused-import
    import urllib
except ImportError:
    pass

IS_HOST = 'typing' in sys.modules

def _is_alphanumeric(character: str):
    return re.match("^[a-zA-Z0-9]+$", character)

def _encode_character(character: str):
    return "".join(["-", str(ord(character)), "-"])

def _decode_character():
    # TODO: Add details
    pass

def encode(payload: str):
    new_payload = ""
    for char in payload:
        if not _is_alphanumeric(char):
            char = _encode_character(char)
        new_payload += char

