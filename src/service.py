from encoding_mappings import (
    ASPIRATED_CYRILLIC_LETTERS,
    ASPIRATED_CYRILLIC_LETTERS_VOICED,
    ASPIRATED_CYRILLIC_LETTERS_VOICELESS,
    ASPIRATED_ROMAN_LETTERS,
    IAST_INPUT_ALIASES,
    RUSSIAN_ENCODINGS,
    Encodings,
)

UKR_ENCODINGS = (Encodings.UKR_G.value, Encodings.UKR_H.value)


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

    # Normalize common non-standard IAST look-alikes to their canonical form before
    # matching (e.g. "ń" U+0144 used for the velar nasal "ṅ" U+1E45 in many song texts).
    if input_encoding == Encodings.IAST.value:
        for wrong, right in IAST_INPUT_ALIASES.items():
            string = string.replace(wrong, right)

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
                if string[j : j + len(key)] == key:
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

    if input_encoding in UKR_ENCODINGS or output_encoding in UKR_ENCODINGS:
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
    temp_symbols = _convert_aspirated_cyrillic_properly(string, output_encoding)
    # This is only for Ukrainian into Russian (change dga into dha) — Russian
    # has no г/х aspirate distinction, so all 10 aspirated stops apply.
    if input_encoding in UKR_ENCODINGS and output_encoding in RUSSIAN_ENCODINGS:
        temp_symbols = _change_ga_to_ha(temp_symbols)
    # UKR_G's aspirated stops are already resolved to г by the base table +
    # the fixup above; converting into UKR_H additionally needs the 5
    # voiceless ones rewritten to х (voiced ones stay г in both schemes).
    elif input_encoding == Encodings.UKR_G.value and output_encoding == Encodings.UKR_H.value:
        temp_symbols = _change_ga_to_ha(temp_symbols, ASPIRATED_CYRILLIC_LETTERS_VOICELESS)
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
    if output_encoding in UKR_ENCODINGS:
        string = string.replace("э", "е")
        string = string.replace("Э", "Е")
    # Replace russian e with Roman e
    else:
        string = string.replace("э", "e")
        string = string.replace("Э", "E")
    return string


def _ends_with_letter(temp_symbols: list, i: int, letters: tuple) -> bool:
    """True if the consonant ending at index i (1 codepoint, or 2 for a
    retroflex letter with a combining dot below, e.g. "т̣") is in 'letters'."""
    if temp_symbols[i].lower() in letters:
        return True
    if i > 0 and (temp_symbols[i - 1] + temp_symbols[i]).lower() in letters:
        return True
    return False


def _change_ga_to_ha(temp_symbols: list, letters: tuple = ASPIRATED_CYRILLIC_LETTERS) -> list:
    """Replace г with х after aspirated consonants (Ukrainian dga → dha pattern).
    'letters' narrows which aspirated stops this applies to — Russian has no
    г/х aspirate distinction so all 10 apply; UKR_G -> UKR_H only rewrites the
    5 voiceless stops, since voiced stops keep г in both Ukrainian schemes."""
    for i in range(len(temp_symbols) - 1):
        if not _ends_with_letter(temp_symbols, i, letters):
            continue
        if temp_symbols[i + 1] == "г":
            temp_symbols[i + 1] = "х"
        elif temp_symbols[i + 1] == "Г":
            temp_symbols[i + 1] = "Х"
    return temp_symbols


def _convert_aspirated_cyrillic_properly(string: str, output_encoding: str = None) -> list:
    """Fix wrong conversions that happen due to overlapping symbols"""
    # 'temp_symbols' is a temporary list of all the symbols in our converted text
    # 'ASPIRATED_CYRILLIC_LETTERS' and 'ASPIRATED_ROMAN_LETTERS' are list of letters corresponding
    # to the aspirated consonants in Sanskrit (Cyrillic and Roman).
    # In UKR_H, voiceless aspirates (kh, ch, .th, th, ph) keep the naive "х"
    # instead of being rewritten to "г"; voiced aspirates always become "г".
    aspirated_to_g = (
        ASPIRATED_CYRILLIC_LETTERS_VOICED if output_encoding == Encodings.UKR_H.value else ASPIRATED_CYRILLIC_LETTERS
    )
    temp_symbols = list(string)
    for i in range(len(temp_symbols) - 1):
        if _ends_with_letter(temp_symbols, i, aspirated_to_g):
            if temp_symbols[i + 1] == "х":
                temp_symbols[i + 1] = "г"
            elif temp_symbols[i + 1] == "Х":
                temp_symbols[i + 1] = "Г"
        if _ends_with_letter(temp_symbols, i, ASPIRATED_ROMAN_LETTERS):
            if temp_symbols[i + 1] == "г":
                temp_symbols[i + 1] = "h"
            elif temp_symbols[i + 1] == "Г":
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
        if string[i : i + 2] == "Дж":
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
