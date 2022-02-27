import re
import gc

try:
    from typing import Dict
except ImportError:
    pass


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


def encode_characters(original: str) -> str:
    payload = ""
    for char in original:
        if not _is_alphanumeric(char):
            char = _encode_character(char)
        payload += char
    gc.collect()
    return payload


def decode_characters(payload: str) -> str:
    translation = ""
    payload_iter = iter(payload)
    for char in payload_iter:
        if char == "-":
            sub_seq = char
            try:
                while True:
                    next_char = next(payload_iter)
                    sub_seq += next_char
                    if next_char == "-":
                        break
            except StopIteration:
                raise RuntimeError("Could not parse a special character in string")
            char = _decode_character(sub_seq)
        translation += char
    gc.collect()
    return translation


def decode_payload(payload: str) -> Dict[str, str]:
    payload_dict = {}
    kv_pairs = payload.split("&")
    for kv_str in kv_pairs:
        key, value = kv_str.split("=")
        key = decode_characters(key)
        value = decode_characters(value)
        payload_dict[key] = value
    gc.collect()
    return payload_dict


def encode_dictionary(payload: Dict[str, str]) -> Dict[str, str]:
    safe_dict = {}
    for key, value in payload.items():
        safe_dict[encode_characters(key)] = encode_characters(value)
    return safe_dict
