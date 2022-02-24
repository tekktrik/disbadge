import sys
import re
import gc


IS_HOST = 'typing' in sys.modules

def _is_alphanumeric(character: str) -> bool:
    return re.match("^[a-zA-Z0-9]+$", character)

def _encode_character(character: str) -> str:

    if not isinstance(character, str):
        raise TypeError("Can only encode a string character")

    return "".join(["-", str(ord(character)), "-"])

def _decode_character(char_str: str) -> str:

    if not isinstance(char_str, str):
        raise TypeError("Can only decode a string representation of a character")
    
    if not char_str.startswith("-") or not char_str.endswith("-"):
        raise ValueError("Not a decodable character string")

    return chr(int(char_str[1:-1]))

def encode(original: str) -> str:
    payload = ""
    for char in original:
        if not _is_alphanumeric(char):
            char = _encode_character(char)
        payload += char
    gc.collect()
    return payload

def decode(payload: str) -> str:
    original = ""
    payload_iter = iter(payload)
    for char in payload_iter:
        if char == "-":
            sub_seq = char
            try:
                while True:
                    next_char = next(payload)
                    sub_seq += next_char
                    if next_char == "-":
                        break
            except StopIteration:
                raise RuntimeError("Could not parse a special character in string")
            char = _decode_character(sub_seq)
        original += char
