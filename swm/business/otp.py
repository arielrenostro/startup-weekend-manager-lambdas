import re
from uuid import uuid4


class OTPCodeDTO:
    code: str = None
    hex_: str = None

    def __init__(self, code, hex_):
        self.code = code
        self.hex_ = hex_

    def __str__(self):
        return f'OTPCode code [{self.code}], hex_ [{self.hex_}]'


CONVERT_TABLE = {
    'a': '0',
    'b': '1',
    'c': '2',
    'd': '3',
    'e': '4',
    'f': '5',
    'g': '6',
    'h': '7',
    'i': '8',
    'j': '9',
    'k': '0',
    'l': '1',
    'm': '2',
    'n': '3',
    'o': '4',
    'p': '5',
    'q': '6',
    'r': '7',
    's': '8',
    't': '9',
    'u': '0',
    'v': '1',
    'w': '2',
    'x': '3',
    'y': '4',
    'z': '5'
}


def _convert_hex_to_code(hex_without_numbers):
    code = ''
    for i in range(6):
        char = hex_without_numbers[i]
        char_code = CONVERT_TABLE[char]
        code = f'{code}{char_code}'
    return code


def generate_code(hex_=None) -> OTPCodeDTO:
    if not hex_:
        while True:
            hex_ = str(uuid4())
            hex_without_numbers = re.sub(r'([0-9]|-)', '', hex_)
            if len(hex_without_numbers) > 5:
                break
    else:
        hex_without_numbers = re.sub(r'([0-9]|-)', '', hex_)

    code = _convert_hex_to_code(hex_without_numbers)
    return OTPCodeDTO(code, hex_)
