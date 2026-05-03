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

    # Build a lookup so we can translate in a single left-to-right pass.
    # str.replace() in a loop causes collisions when one encoding reuses a
    # character that was already written as output (e.g. IAST ṣ→ñ then ñ→ï
    # in Balaram would corrupt the earlier ñ output).
    translation = {}
    for i, item in enumerate(input_characters):
        if item != output_characters[i] and item not in translation:
            translation[item] = output_characters[i]

    if translation:
        # Sort by length descending so multi-char tokens (e.g. Velthuis "aa")
        # are matched before their single-char prefixes.
        sorted_keys = sorted(translation, key=len, reverse=True)
        result = []
        j = 0
        while j < len(string):
            for key in sorted_keys:
                if string[j:j + len(key)] == key:
                    result.append(translation[key])
                    j += len(key)
                    break
            else:
                result.append(string[j])
                j += 1
        string = "".join(result)

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
    converted_text = "".join(temp_symbols)
    return converted_text


def _change_anusvara_type(string):
    string = string.replace("ṁ", "ṃ")
    string = string.replace("Ṁ", "Ṃ")
    string = string.replace("м̇", "м̣")
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
    """Replace г with х after aspirated consonants (Ukrainian dga → dha pattern)"""
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
    """Upgrades Дж to ДЖ only in an all-caps context (e.g. JAGANNATHA -> ДЖАҐАННАТГА)."""
    result = []
    i = 0
    while i < len(string):
        if string[i:i + 2] == "Дж":
            next_is_upper = (i + 2 < len(string)) and string[i + 2].isupper()
            if next_is_upper:
                result.append("ДЖ")
            else:
                result.append("Дж")
            i += 2
        else:
            result.append(string[i])
            i += 1
    return "".join(result)
