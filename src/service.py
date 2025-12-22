from encoding_mappings import (
    ASPIRATED_CYRILLIC_LETTERS,
    ASPIRATED_ROMAN_LETTERS,
    RUSSIAN_ENCODINGS,
    Encodings,
)


def convert(
    string: str,
    input_characters: tuple,
    output_characters: tuple,
    input_encoding: str,
    output_encoding: str,
    change_anusvara: bool = False,
) -> str:
    """
    This is the main method which converts between encodings.

    Args:
        string (str): input text to convert into another encoding
        input_characters (list): list with all symbols of the original encoding
            (each in its own place, index matters!)
        output_characters (list): list with all corresponding symbols of the target encoding
            (each in its own respective place, index matters!)
        input_encoding (str): Name of the original encoding
        output_encoding (str): Name of the target encoding
        change_anusvara (bool): To use the dot above or under m
    """

    if input_encoding == output_encoding:
        return string

    for i, item in enumerate(input_characters):
        if item in string and item != output_characters[i]:
            string = string.replace(item, output_characters[i])

    if input_encoding == Encodings.HK.value:
        string = string.lower()

    if change_anusvara:
        string = _change_anusvara_type(string)

    if input_encoding == Encodings.UKR.value or output_encoding == Encodings.UKR.value:
        string = _convert_ukrainian(string, input_encoding, output_encoding)

    if input_encoding in RUSSIAN_ENCODINGS and output_encoding not in RUSSIAN_ENCODINGS:
        string = _replace_russian_e(string, output_encoding)

    if output_encoding in RUSSIAN_ENCODINGS:
        string = _fix_russian_e_at_beginning(string)

    # Set proper case for 'Дж'
    if "Дж" in string:
        string = _convert_j_properly(string)

    return string


def _convert_ukrainian(string, input_encoding, output_encoding):
    # 'temp_symbols' is a temporary list of all the symbols in our converted text
    temp_symbols = _convert_aspirated_cyrillic_properly(string)
    # This is only for Ukrainian into Russian (change dga into dha)
    if input_encoding == Encodings.UKR.value and output_encoding in RUSSIAN_ENCODINGS:
        temp_symbols = _change_ga_to_ha(temp_symbols)
        # 'x' is the joined list 's' (original converted text
        # but now with all necessary transormations)
    converted_text = "".join(temp_symbols)
    return converted_text


def _change_anusvara_type(string):
    if "ṁ" in string:
        string = string.replace("ṁ", "ṃ")
    elif "Ṁ" in string:
        string = string.replace("Ṁ", "Ṃ")
    elif "м̇" in string:
        string = string.replace("м̇", "м̣")
    elif "М̇" in string:
        string = string.replace("М̇", "М̣")
    return string


def _replace_russian_e(string, output_encoding):
    # Replace russian e with Ukrainian e
    if output_encoding == Encodings.UKR.value:
        string = string.replace("э", "е")
        string = string.replace("Э", "Е")
    # Replace russian e with Roman e
    else:
        string = string.replace("э", "e")
        string = string.replace("Э", "E")
    return string


def _change_ga_to_ha(temp_symbols: list) -> list:
    """Change гг to гх in cyrillic"""
    for i in range(len(temp_symbols) - 1):
        if temp_symbols[i].lower() in ASPIRATED_CYRILLIC_LETTERS and temp_symbols[i + 1] == "г":
            temp_symbols[i + 1] = "х"
        elif temp_symbols[i].lower() in ASPIRATED_CYRILLIC_LETTERS and temp_symbols[i + 1] == "Г":
            temp_symbols[i + 1] = "Х"
    return temp_symbols


def _convert_aspirated_cyrillic_properly(string: str) -> list:
    """Fix wrong conversions that happen due to overlapping symbols"""
    # 'temp_symbols' is a temporary list of all the symbols in our converted text
    # 'ASPIRATED_CYRILLIC_LETTERS' and 'ASPIRATED_ROMAN_LETTERS' are list of letters corresponding
    # to the aspirated consonants in Sanskrit (Cyrillic and Roman).
    temp_symbols = list(string)
    for i in range(len(temp_symbols) - 1):
        if temp_symbols[i].lower() in ASPIRATED_CYRILLIC_LETTERS and temp_symbols[i + 1] == "х":
            temp_symbols[i + 1] = "г"
        elif temp_symbols[i].lower() in ASPIRATED_CYRILLIC_LETTERS and temp_symbols[i + 1] == "Х":
            temp_symbols[i + 1] = "Г"
        if temp_symbols[i].lower() in ASPIRATED_ROMAN_LETTERS and temp_symbols[i + 1] == "г":
            temp_symbols[i + 1] = "h"
        elif temp_symbols[i].lower() in ASPIRATED_ROMAN_LETTERS and temp_symbols[i + 1] == "Г":
            temp_symbols[i + 1] = "H"
    return temp_symbols


def _fix_russian_e_at_beginning(string: str) -> str:
    """Replaces е with э at the beginning of a word"""
    if string.startswith("е"):
        string = string.replace("е", "э", 1)
    if string.startswith("Е"):
        string = string.replace("Е", "Э", 1)
    if "\nе" in string:
        string = string.replace("\nе", "\nэ")
    if "\nЕ" in string:
        string = string.replace("\nЕ", "\nЭ")
    if " е" in string:
        string = string.replace(" е", " э")
    if " Е" in string:
        string = string.replace(" Е", " Э")
    return string


def _convert_j_properly(string: str) -> str:
    """Converts j to cyrillic дж"""
    try:
        position = 0
        # Check if the next character after "Дж" is uppercase
        while string != "Дж" and position != -1:
            if string[position:].startswith("Дж") and string[position + 2].isupper():
                string = string[:position] + "ДЖ" + string[position + 2 :]
            # Move past the current "Дж" to find the next occurrence
            position = string.find("Дж", position + 1)
    except IndexError:
        string = string[:-1] + "Ж"
    return string
