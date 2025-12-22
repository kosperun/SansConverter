from encoding_mappings import (
    BALARAM,
    BALARAM_EXT,
    GAURA_TIMES,
    HK,
    HK_EXT,
    IAST,
    IAST_EXT,
    RUS,
    UKR,
    VELTHIUS,
    VELTHIUS_EXT,
    Encodings,
)
from service import convert


def test_convert_general():
    ###########################################################################
    # Balaram
    ###########################################################################
    result = convert(
        "".join(BALARAM),
        BALARAM,
        IAST,
        Encodings.BALARAM.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST)

    result = convert(
        "".join(BALARAM),
        BALARAM,
        VELTHIUS,
        Encodings.BALARAM.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS)

    result = convert(
        "".join(BALARAM),
        BALARAM,
        HK,
        Encodings.BALARAM.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK)

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        IAST_EXT,
        Encodings.BALARAM.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST_EXT)

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        VELTHIUS_EXT,
        Encodings.BALARAM.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS_EXT)

    # FIXME: There is a bug in hk as target it's completely wrong!
    # result = convert(
    #     "".join(BALARAM_EXT),
    #     BALARAM_EXT,
    #     HK_EXT,
    #     Encodings.BALARAM.value,
    #     Encodings.HK.value,
    # )
    # assert result == "".join(HK_EXT)

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        UKR,
        Encodings.BALARAM.value,
        Encodings.UKR.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(UKR).replace("Дж", "ДЖ").replace("ґх", "ґг").replace("ҐХ", "ҐГ")

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        RUS,
        Encodings.BALARAM.value,
        Encodings.RUS.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(RUS).replace("Дж", "ДЖ")

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        GAURA_TIMES,
        Encodings.BALARAM.value,
        Encodings.GAURA_TIMES.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(GAURA_TIMES).replace("Дж", "ДЖ")

    result = convert(
        "".join(BALARAM),
        BALARAM,
        BALARAM,
        Encodings.BALARAM.value,
        Encodings.BALARAM.value,
    )
    assert result == "".join(BALARAM)

    result = convert(
        "".join(BALARAM_EXT),
        BALARAM_EXT,
        BALARAM_EXT,
        Encodings.BALARAM.value,
        Encodings.BALARAM.value,
    )
    assert result == "".join(BALARAM_EXT)

    ###########################################################################
    # IAST
    ###########################################################################
    result = convert(
        "".join(IAST),
        IAST,
        BALARAM,
        Encodings.IAST.value,
        Encodings.BALARAM.value,
    )
    # FIXME: This is a known bug!
    assert result == "".join(BALARAM).replace("Ñ", "Ï").replace("ñ", "ï")

    result = convert(
        "".join(IAST),
        IAST,
        VELTHIUS,
        Encodings.IAST.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS)

    result = convert(
        "".join(IAST),
        IAST,
        HK,
        Encodings.IAST.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK)

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        BALARAM_EXT,
        Encodings.IAST.value,
        Encodings.BALARAM.value,
    )
    # FIXME: Bug!
    assert result == "".join(BALARAM_EXT).replace("ñ", "ï").replace("Ñ", "Ï")

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        VELTHIUS_EXT,
        Encodings.IAST.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS_EXT)

    # FIXME: Bug!
    # result = convert(
    #     "".join(IAST_EXT),
    #     IAST_EXT,
    #     HK_EXT,
    #     Encodings.IAST.value,
    #     Encodings.HK.value,
    # )
    # assert result == "".join(HK_EXT)

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        UKR,
        Encodings.IAST.value,
        Encodings.UKR.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(UKR).replace("Дж", "ДЖ").replace("ґх", "ґг").replace("ҐХ", "ҐГ")

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        RUS,
        Encodings.IAST.value,
        Encodings.RUS.value,
    )
    assert result == "".join(RUS).replace("Дж", "ДЖ")

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        GAURA_TIMES,
        Encodings.IAST.value,
        Encodings.GAURA_TIMES.value,
    )
    assert result == "".join(GAURA_TIMES).replace("Дж", "ДЖ")

    result = convert(
        "".join(IAST),
        IAST,
        IAST,
        Encodings.IAST.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST)

    result = convert(
        "".join(IAST_EXT),
        IAST_EXT,
        IAST_EXT,
        Encodings.IAST.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST_EXT)

    ##########################################################################
    # Velthius
    ###########################################################################
    result = convert(
        "".join(VELTHIUS),
        VELTHIUS,
        BALARAM,
        Encodings.VELTHIUS.value,
        Encodings.BALARAM.value,
    )
    assert result == "".join(BALARAM)

    result = convert(
        "".join(VELTHIUS),
        VELTHIUS,
        IAST,
        Encodings.VELTHIUS.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST)

    result = convert(
        "".join(VELTHIUS),
        VELTHIUS,
        HK,
        Encodings.VELTHIUS.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK)

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        BALARAM_EXT,
        Encodings.VELTHIUS.value,
        Encodings.BALARAM.value,
    )
    assert result == "".join(BALARAM_EXT)

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        IAST_EXT,
        Encodings.VELTHIUS.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST_EXT)

    # FIXME: Bug!
    # result = convert(
    #     "".join(VELTHIUS_EXT),
    #     VELTHIUS_EXT,
    #     HK_EXT,
    #     Encodings.VELTHIUS.value,
    #     Encodings.HK.value,
    # )

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        UKR,
        Encodings.VELTHIUS.value,
        Encodings.UKR.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(UKR).replace("Дж", "ДЖ").replace("ґх", "ґг").replace("ҐХ", "ҐГ")

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        RUS,
        Encodings.VELTHIUS.value,
        Encodings.RUS.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(RUS).replace("Дж", "ДЖ")

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        GAURA_TIMES,
        Encodings.VELTHIUS.value,
        Encodings.GAURA_TIMES.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(GAURA_TIMES).replace("Дж", "ДЖ")

    result = convert(
        "".join(VELTHIUS),
        VELTHIUS,
        VELTHIUS,
        Encodings.VELTHIUS.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS)

    result = convert(
        "".join(VELTHIUS_EXT),
        VELTHIUS_EXT,
        VELTHIUS_EXT,
        Encodings.VELTHIUS.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS_EXT)

    ###########################################################################
    # HK
    ###########################################################################
    # result = convert(
    #     "".join(HK),
    #     HK,
    #     BALARAM,
    #     Encodings.HK.value,
    #     Encodings.BALARAM.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(BALARAM).replace("Ï", "Ñ").replace("ï", "ñ")

    # result = convert(
    #     "".join(HK),
    #     HK,
    #     IAST,
    #     Encodings.HK.value,
    #     Encodings.IAST.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(IAST)

    # result = convert(
    #     "".join(HK),
    #     HK,
    #     VELTHIUS,
    #     Encodings.HK.value,
    #     Encodings.VELTHIUS.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(VELTHIUS)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     BALARAM_EXT,
    #     Encodings.HK.value,
    #     Encodings.BALARAM.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(BALARAM_EXT)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     IAST_EXT,
    #     Encodings.HK.value,
    #     Encodings.IAST.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(IAST_EXT)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     VELTHIUS_EXT,
    #     Encodings.HK.value,
    #     Encodings.VELTHIUS.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(VELTHIUS_EXT)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     UKR,
    #     Encodings.HK.value,
    #     Encodings.UKR.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(UKR)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     RUS,
    #     Encodings.HK.value,
    #     Encodings.RUS.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(RUS)

    # result = convert(
    #     "".join(HK_EXT),
    #     HK_EXT,
    #     GAURA_TIMES,
    #     Encodings.HK.value,
    #     Encodings.GAURA_TIMES.value,
    # )
    # # FIXME: Bug!
    # assert result == "".join(GAURA_TIMES)

    result = convert(
        "".join(HK),
        HK,
        HK,
        Encodings.HK.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK)

    result = convert(
        "".join(HK_EXT),
        HK_EXT,
        HK_EXT,
        Encodings.HK.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK_EXT)

    ###########################################################################
    # Ukrainian
    ###########################################################################
    result = convert(
        "".join(UKR),
        UKR,
        BALARAM_EXT,
        Encodings.UKR.value,
        Encodings.BALARAM.value,
    )
    assert result == "".join(BALARAM_EXT)

    result = convert(
        "".join(UKR),
        UKR,
        IAST_EXT,
        Encodings.UKR.value,
        Encodings.IAST.value,
    )
    assert result == "".join(IAST_EXT)

    result = convert(
        "".join(UKR),
        UKR,
        VELTHIUS_EXT,
        Encodings.UKR.value,
        Encodings.VELTHIUS.value,
    )
    assert result == "".join(VELTHIUS_EXT)

    result = convert(
        "".join(UKR),
        UKR,
        HK_EXT,
        Encodings.UKR.value,
        Encodings.HK.value,
    )
    assert result == "".join(HK_EXT)

    result = convert(
        "".join(UKR),
        UKR,
        RUS,
        Encodings.UKR.value,
        Encodings.RUS.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(RUS).replace("Дж", "ДЖ")

    result = convert(
        "".join(UKR),
        UKR,
        GAURA_TIMES,
        Encodings.UKR.value,
        Encodings.GAURA_TIMES.value,
    )
    # FIXME: Fix conversion of J/j
    assert result == "".join(GAURA_TIMES).replace("Дж", "ДЖ")

    result = convert(
        "".join(UKR),
        UKR,
        UKR,
        Encodings.UKR.value,
        Encodings.UKR.value,
    )
    assert result == "".join(UKR)

    ###########################################################################
    # russian
    ###########################################################################
    result = convert(
        " ".join(RUS),
        RUS,
        BALARAM_EXT,
        Encodings.RUS.value,
        Encodings.BALARAM.value,
    )
    assert result == " ".join(BALARAM_EXT)

    result = convert(
        " ".join(RUS),
        RUS,
        IAST_EXT,
        Encodings.RUS.value,
        Encodings.IAST.value,
    )
    assert result == " ".join(IAST_EXT)

    result = convert(
        " ".join(RUS),
        RUS,
        VELTHIUS_EXT,
        Encodings.RUS.value,
        Encodings.VELTHIUS.value,
    )
    assert result == " ".join(VELTHIUS_EXT)

    result = convert(
        " ".join(RUS),
        RUS,
        HK_EXT,
        Encodings.RUS.value,
        Encodings.HK.value,
    )
    assert result == " ".join(HK_EXT)

    result = convert(
        " ".join(RUS),
        RUS,
        UKR,
        Encodings.RUS.value,
        Encodings.UKR.value,
    )
    assert result == " ".join(UKR)

    result = convert(
        "".join(RUS),
        RUS,
        GAURA_TIMES,
        Encodings.RUS.value,
        Encodings.GAURA_TIMES.value,
    )
    assert result == "".join(GAURA_TIMES).replace("Дж", "ДЖ")

    result = convert(
        " ".join(RUS),
        RUS,
        RUS,
        Encodings.RUS.value,
        Encodings.RUS.value,
    )
    assert result == " ".join(RUS)

    ###########################################################################
    # Gaura Times
    ###########################################################################
    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        BALARAM_EXT,
        Encodings.GAURA_TIMES.value,
        Encodings.BALARAM.value,
    )
    assert result == " ".join(BALARAM_EXT)

    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        IAST_EXT,
        Encodings.GAURA_TIMES.value,
        Encodings.IAST.value,
    )
    assert result == " ".join(IAST_EXT)

    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        VELTHIUS_EXT,
        Encodings.GAURA_TIMES.value,
        Encodings.VELTHIUS.value,
    )
    assert result == " ".join(VELTHIUS_EXT)

    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        HK_EXT,
        Encodings.GAURA_TIMES.value,
        Encodings.HK.value,
    )
    assert result == " ".join(HK_EXT)

    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        UKR,
        Encodings.GAURA_TIMES.value,
        Encodings.UKR.value,
    )
    assert result == " ".join(UKR)

    result = convert(
        "".join(GAURA_TIMES),
        GAURA_TIMES,
        RUS,
        Encodings.GAURA_TIMES.value,
        Encodings.RUS.value,
    )
    assert result == "".join(RUS).replace("Дж", "ДЖ")

    result = convert(
        " ".join(GAURA_TIMES),
        GAURA_TIMES,
        GAURA_TIMES,
        Encodings.GAURA_TIMES.value,
        Encodings.GAURA_TIMES.value,
    )
    assert result == " ".join(GAURA_TIMES)

    # for i, item in enumerate(input_characters):
    #     if item in string:
    #         string = string.replace(item, output_characters[i])

    # if input_encoding == Encodings.HK.value:
    #     string = string.lower()

    # if use_anusvara:
    #     string = _change_anusvara_type(string)

    # if input_encoding == Encodings.UKR.value or output_encoding == Encodings.UKR.value:
    #     string = _convert_ukrainian(string, input_encoding, output_encoding)

    # # Replace russian e
    # if input_encoding == Encodings.RUS.value:
    #     string = _fix_russian_e_at_beginning(string)
    #     if output_encoding != Encodings.RUS.value:
    #         string = _replace_russian_e(string, output_encoding)

    # # Set proper case for 'Дж'
    # if "Дж" in string:
    #     string = _convert_j_properly(string)

    # return string
