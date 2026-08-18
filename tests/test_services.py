"""
Tests for service.convert().

Each test calls convert() directly with explicit input/output character tuples,
exactly as sans_converter.py does. Every test covers all 15 diacritical
characters (and uppercase where the encoding supports it) so no mapping can be
silently skipped.

HK is lowercase-only by design — HK output tests use only the lowercase half
of the tuples (indices 0-14).
"""

import pytest

from encoding_mappings import (
    ALL_EXT_ENCODINGS,
    BALARAM,
    BALARAM_EXT,
    GAURA_TIMES,
    HK,
    HK_EXT,
    IAST,
    IAST_EXT,
    RUS,
    UKR_G,
    UKR_H,
    VELTHUIS,
    VELTHUIS_EXT,
    Encodings,
)
from service import convert

B = Encodings.BALARAM.value
I = Encodings.IAST.value  # noqa E741
H = Encodings.HK.value
V = Encodings.VELTHUIS.value
UG = Encodings.UKR_G.value
UH = Encodings.UKR_H.value
R = Encodings.RUS.value
G = Encodings.GAURA_TIMES.value


def lc(t):
    """Join only the lowercase half of a basic encoding tuple (indices 0-14)."""
    return "".join(t[:15])


def full(t):
    """Join the full tuple."""
    return "".join(t)


# ---------------------------------------------------------------------------
# Roman basic tuples (IAST, BALARAM, VELTHUIS, HK) — all 15 diacritical chars
# ---------------------------------------------------------------------------


class TestRomanBasic:
    def test_iast_to_balaram(self):
        assert convert(full(IAST), IAST, BALARAM, I, B) == full(BALARAM)

    def test_balaram_to_iast(self):
        assert convert(full(BALARAM), BALARAM, IAST, B, I) == full(IAST)

    def test_iast_to_velthuis(self):
        assert convert(full(IAST), IAST, VELTHUIS, I, V) == full(VELTHUIS)

    def test_velthuis_to_iast(self):
        assert convert(full(VELTHUIS), VELTHUIS, IAST, V, I) == full(IAST)

    def test_balaram_to_velthuis(self):
        assert convert(full(BALARAM), BALARAM, VELTHUIS, B, V) == full(VELTHUIS)

    def test_velthuis_to_balaram(self):
        assert convert(full(VELTHUIS), VELTHUIS, BALARAM, V, B) == full(BALARAM)

    def test_iast_to_hk(self):
        assert convert(lc(IAST), IAST, HK, I, H) == lc(HK)

    def test_hk_to_iast(self):
        assert convert(lc(HK), HK, IAST, H, I) == lc(IAST)

    def test_balaram_to_hk(self):
        assert convert(lc(BALARAM), BALARAM, HK, B, H) == lc(HK)

    def test_hk_to_balaram(self):
        assert convert(lc(HK), HK, BALARAM, H, B) == lc(BALARAM)

    def test_velthuis_to_hk(self):
        assert convert(lc(VELTHUIS), VELTHUIS, HK, V, H) == lc(HK)

    def test_hk_to_velthuis(self):
        assert convert(lc(HK), HK, VELTHUIS, H, V) == lc(VELTHUIS)


# ---------------------------------------------------------------------------
# Roman extended tuples — all chars including uppercase
# ---------------------------------------------------------------------------


class TestRomanExt:
    def test_iast_ext_to_balaram_ext(self):
        assert convert(full(IAST_EXT), IAST_EXT, BALARAM_EXT, I, B) == full(BALARAM_EXT)

    def test_balaram_ext_to_iast_ext(self):
        assert convert(full(BALARAM_EXT), BALARAM_EXT, IAST_EXT, B, I) == full(IAST_EXT)

    def test_iast_ext_to_velthuis_ext(self):
        assert convert(full(IAST_EXT), IAST_EXT, VELTHUIS_EXT, I, V) == full(VELTHUIS_EXT)

    def test_velthuis_ext_to_iast_ext(self):
        assert convert(full(VELTHUIS_EXT), VELTHUIS_EXT, IAST_EXT, V, I) == full(IAST_EXT)

    def test_balaram_ext_to_velthuis_ext(self):
        assert convert(full(BALARAM_EXT), BALARAM_EXT, VELTHUIS_EXT, B, V) == full(VELTHUIS_EXT)

    def test_velthuis_ext_to_balaram_ext(self):
        assert convert(full(VELTHUIS_EXT), VELTHUIS_EXT, BALARAM_EXT, V, B) == full(BALARAM_EXT)


# ---------------------------------------------------------------------------
# Roman extended -> Cyrillic (space-separated to avoid Russian е/э
# word-boundary logic firing between adjacent characters)
# ---------------------------------------------------------------------------


class TestRomanToCyrillic:
    # Space-separated input is used to cover all characters, but two side effects
    # apply: (1) word-initial е becomes э in Russian due to _fix_russian_e_at_beginning,
    # so the expected output replaces 'Е' and 'е' with 'Э' and 'э' at word boundaries;
    # (2) uppercase J maps to Дж (title-case) not ДЖ, so both J slots in the tuple
    # produce Дж in the expected output.

    def _rus_expected(self, sep=" "):
        return sep.join(RUS).replace(" Е ", " Э ").replace(" е ", " э ")

    def test_iast_ext_to_rus(self):
        expected = " ".join(RUS).replace("Дж ДЖ", "Дж Дж").replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(IAST_EXT), IAST_EXT, RUS, I, R) == expected

    def test_iast_ext_to_ukr(self):
        expected = " ".join(UKR_G).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(IAST_EXT), IAST_EXT, UKR_G, I, UG) == expected

    def test_balaram_ext_to_rus(self):
        expected = " ".join(RUS).replace("Дж ДЖ", "Дж Дж").replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(BALARAM_EXT), BALARAM_EXT, RUS, B, R) == expected

    def test_balaram_ext_to_ukr(self):
        expected = " ".join(UKR_G).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(BALARAM_EXT), BALARAM_EXT, UKR_G, B, UG) == expected

    def test_velthuis_ext_to_rus(self):
        expected = " ".join(RUS).replace("Дж ДЖ", "Дж Дж").replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(VELTHUIS_EXT), VELTHUIS_EXT, RUS, V, R) == expected

    def test_velthuis_ext_to_ukr(self):
        expected = " ".join(UKR_G).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(VELTHUIS_EXT), VELTHUIS_EXT, UKR_G, V, UG) == expected


# ---------------------------------------------------------------------------
# Cyrillic -> Roman extended
# ---------------------------------------------------------------------------


class TestCyrillicToRoman:
    def test_ukr_to_iast_ext(self):
        assert convert(full(UKR_G), UKR_G, IAST_EXT, UG, I) == full(IAST_EXT)

    def test_ukr_to_balaram_ext(self):
        assert convert(full(UKR_G), UKR_G, BALARAM_EXT, UG, B) == full(BALARAM_EXT)

    def test_ukr_to_velthuis_ext(self):
        assert convert(full(UKR_G), UKR_G, VELTHUIS_EXT, UG, V) == full(VELTHUIS_EXT)

    def test_ukr_to_hk_ext(self):
        assert convert(full(UKR_G), UKR_G, HK_EXT, UG, H) == full(HK_EXT)

    def test_rus_to_iast_ext(self):
        assert convert(" ".join(RUS), RUS, IAST_EXT, R, I) == " ".join(IAST_EXT)

    def test_rus_to_balaram_ext(self):
        assert convert(" ".join(RUS), RUS, BALARAM_EXT, R, B) == " ".join(BALARAM_EXT)

    def test_rus_to_velthuis_ext(self):
        assert convert(" ".join(RUS), RUS, VELTHUIS_EXT, R, V) == " ".join(VELTHUIS_EXT)

    def test_rus_to_hk_ext(self):
        assert convert(" ".join(RUS), RUS, HK_EXT, R, H) == " ".join(HK_EXT)


# ---------------------------------------------------------------------------
# Cyrillic <-> Cyrillic
# ---------------------------------------------------------------------------


class TestCyrillicToCyrillic:
    def test_ukr_to_rus(self):
        # UKR_G has Дж and ДЖ as separate entries; space-separated means Дж is
        # followed by a space so _convert_j_properly does not upgrade it.
        # е at word start becomes э in Russian.
        expected = " ".join(RUS).replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(UKR_G), UKR_G, RUS, UG, R) == expected

    def test_rus_to_ukr(self):
        assert convert(" ".join(RUS), RUS, UKR_G, R, UG) == " ".join(UKR_G)

    def test_ukr_to_gaura_times(self):
        # е at word start becomes э via _fix_russian_e_at_beginning (GAURA_TIMES
        # is in RUSSIAN_ENCODINGS)
        expected = " ".join(GAURA_TIMES).replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(UKR_G), UKR_G, GAURA_TIMES, UG, G) == expected

    def test_gaura_times_to_ukr(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, UKR_G, G, UG) == " ".join(UKR_G)

    def test_rus_to_gaura_times(self):
        assert convert(" ".join(RUS), RUS, GAURA_TIMES, R, G) == " ".join(GAURA_TIMES).replace(" Е ", " Э ").replace(
            " е ", " э "
        )

    def test_gaura_times_to_rus(self):
        # е at word start becomes э in Russian
        expected = " ".join(RUS).replace(" Е ", " Э ").replace(" е ", " э ")
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, RUS, G, R) == expected


# ---------------------------------------------------------------------------
# Gaura Times -> Roman
# ---------------------------------------------------------------------------


class TestGauraTimesToRoman:
    def test_gaura_times_to_iast_ext(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, IAST_EXT, G, I) == " ".join(IAST_EXT)

    def test_gaura_times_to_balaram_ext(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, BALARAM_EXT, G, B) == " ".join(BALARAM_EXT)

    def test_gaura_times_to_velthuis_ext(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, VELTHUIS_EXT, G, V) == " ".join(VELTHUIS_EXT)

    def test_gaura_times_to_hk_ext(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, HK_EXT, G, H) == " ".join(HK_EXT)


# ---------------------------------------------------------------------------
# Identity: same encoding returns input unchanged
# ---------------------------------------------------------------------------


class TestIdentity:
    def test_balaram(self):
        assert convert(full(BALARAM), BALARAM, BALARAM, B, B) == full(BALARAM)

    def test_iast(self):
        assert convert(full(IAST), IAST, IAST, I, I) == full(IAST)

    def test_velthuis(self):
        assert convert(full(VELTHUIS), VELTHUIS, VELTHUIS, V, V) == full(VELTHUIS)

    def test_hk(self):
        assert convert(full(HK), HK, HK, H, H) == full(HK)

    def test_ukr(self):
        assert convert(full(UKR_G), UKR_G, UKR_G, UG, UG) == full(UKR_G)

    def test_rus(self):
        assert convert(" ".join(RUS), RUS, RUS, R, R) == " ".join(RUS)

    def test_gaura_times(self):
        assert convert(" ".join(GAURA_TIMES), GAURA_TIMES, GAURA_TIMES, G, G) == " ".join(GAURA_TIMES)


# ---------------------------------------------------------------------------
# IAST -> Balaram ṣ/ñ collision (the previously broken case)
# ---------------------------------------------------------------------------


class TestJCyrillic:
    @pytest.mark.parametrize(
        "inp,enc_out,expected",
        [
            ("jagannatha", UG, "джаґаннатга"),
            ("Jagannatha", UG, "Джаґаннатга"),
            ("JAGANNATHA", UG, "ДЖАҐАННАТГА"),
            ("jagannatha", R, "джаганнатха"),
            ("Jagannatha", R, "Джаганнатха"),
            ("JAGANNATHA", R, "ДЖАГАННАТХА"),
        ],
    )
    def test_j_capitalisation(self, inp, enc_out, expected):
        assert convert(inp, IAST_EXT, ALL_EXT_ENCODINGS[enc_out], I, enc_out) == expected

    def test_mixed_sequence(self):
        inp = "JJjJJjJJjJJjJjJjJjJjJjJ"
        expected = "ДЖДжджДЖДжджДЖДжджДЖДжджДжджДжджДжджДжджДжджДж"
        assert convert(inp, IAST_EXT, UKR_G, I, UG) == expected


class TestIASTToBalaram:
    def test_sibilant_only(self):
        assert convert("puruṣa", IAST, BALARAM, I, B) == "puruña"

    def test_palatal_only(self):
        assert convert("jñāna", IAST, BALARAM, I, B) == "jïäna"

    def test_sibilant_and_palatal_no_collision(self):
        assert convert("jñāna puruṣa", IAST, BALARAM, I, B) == "jïäna puruña"

    def test_visnu(self):
        assert convert("viṣṇu", IAST, BALARAM, I, B) == "viñëu"

    def test_krsna(self):
        assert convert("kṛṣṇa", IAST, BALARAM, I, B) == "kåñëa"


# ---------------------------------------------------------------------------
# Velthuis multi-character token tests
# ---------------------------------------------------------------------------


class TestVelthuisTokens:
    @pytest.mark.parametrize(
        "velthuis,expected_iast",
        [
            ("aa", "ā"),
            ("ii", "ī"),
            ("uu", "ū"),
            (".l", "ḷ"),
            (".rr", "ṝ"),
            (".r", "ṛ"),
            (".s", "ṣ"),
            ('"n', "ṅ"),
            ("~n", "ñ"),
            (".t", "ṭ"),
            (".d", "ḍ"),
            (".n", "ṇ"),
            ('"s', "ś"),
            (".h", "ḥ"),
            (".m", "ṁ"),
        ],
    )
    def test_each_token_to_iast(self, velthuis, expected_iast):
        assert convert(velthuis, VELTHUIS, IAST, V, I) == expected_iast

    def test_dot_rr_not_confused_with_dot_r(self):
        # .rr must match before .r so ṝ is not read as ṛ + r
        assert convert(".rr", VELTHUIS, IAST, V, I) == "ṝ"
        assert convert(".r", VELTHUIS, IAST, V, I) == "ṛ"

    def test_multiple_tokens_in_sequence(self):
        # All 15 tokens in one string, space-separated, matching the full tuple
        velthuis_all = " ".join(VELTHUIS[:15])
        iast_all = " ".join(IAST[:15])
        assert convert(velthuis_all, VELTHUIS, IAST, V, I) == iast_all


# ---------------------------------------------------------------------------
# Anusvara toggle
# ---------------------------------------------------------------------------


class TestAnusvara:
    # change_anusvara fires after translation, so it only takes effect when the
    # output encoding contains ṁ/ṃ — i.e. when converting TO IAST.

    def test_lowercase_dot_above_to_dot_below(self):
        assert convert("raama.m", VELTHUIS, IAST, V, I, change_anusvara=True) == "rāmaṃ"

    def test_uppercase_dot_above_to_dot_below(self):
        assert convert("RAAMA.M", VELTHUIS, IAST, V, I, change_anusvara=True) == "RĀMAṂ"

    def test_mixed_case_both_converted(self):
        # Both uppercase and lowercase anusvara must be converted in the same string
        assert convert("RAAMA.M raama.m", VELTHUIS, IAST, V, I, change_anusvara=True) == "RĀMAṂ rāmaṃ"

    def test_no_change_without_flag(self):
        assert convert("raama.m", VELTHUIS, IAST, V, I, change_anusvara=False) == "rāmaṁ"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_string(self):
        assert convert("", IAST, BALARAM, I, B) == ""

    def test_plain_ascii_passthrough(self):
        assert convert("abcde xyz", IAST, BALARAM, I, B) == "abcde xyz"

    def test_numbers_and_punctuation_passthrough(self):
        assert convert("123, ok!", IAST, BALARAM, I, B) == "123, ok!"

    def test_newline_preserved(self):
        assert convert("kṛṣṇa\nrāma", IAST, BALARAM, I, B) == "kåñëa\nräma"


# Real VedaBase Russian input (issue #7)
#
# Russian VedaBase writes long "ā" as Cyrillic "а"/"А" (U+0430/U+0410) + COMBINING
# MACRON (U+0304), because Cyrillic А has no precomposed macron form in Unicode.
# These strings are copied verbatim from vedabase.io/ru; they must convert with no
# stray combining marks left behind.
# ---------------------------------------------------------------------------

COMBINING_MARKS = ("̄", "̣", "́", "̇", "̃", "Ā", "ā")


def _has_orphan_marks(text):
    """True if any combining diacritic or Latin a-macron survived a Cyrillic->Gaura pass."""
    return any(mark in text for mark in COMBINING_MARKS)


class TestVedabaseRussianLongA:
    def test_long_a_lowercase_converts(self):
        # "ува̄ча" = у в а + U+0304 ч а  -> the macron must be consumed
        out = convert("ува̄ча", RUS, GAURA_TIMES, R, G)
        assert not _has_orphan_marks(out)
        assert out == "увча"

    def test_long_a_uppercase_word_initial(self):
        # "А̄ди" = А + U+0304 д и  (word-initial capital long A)
        out = convert("А̄ди", RUS, GAURA_TIMES, R, G)
        assert not _has_orphan_marks(out)
        assert out == "ди"

    def test_full_verse_no_orphan_marks(self):
        # Bhagavad-gītā 1.1, first line, verbatim from vedabase.io/ru
        verse = "дхр̣тара̄шт̣ра ува̄ча"
        out = convert(verse, RUS, GAURA_TIMES, R, G)
        assert not _has_orphan_marks(out)

    @pytest.mark.parametrize(
        "incoming, out",
        [
            (chr(int("0430", 16)) + chr(int("0304", 16)), chr(int("0101", 16))),
            (chr(int("0410", 16)) + chr(int("0304", 16)), chr(int("0100", 16))),
        ],
        ids=["Lowercase a", "Uppercase A"],
    )
    def test_long_a_roundtrip_rus_iast(self, incoming, out):
        # RUS long-a must map to IAST U+0101 and back to the Cyrillic combining form
        # U+0430 is CYRILLIC SMALL LETTER A
        # U+0410 is CYRILLIC CAPITAL LETTER A
        # U+0304 is COMBINING MACRON
        # U+0101 is LATIN SMALL LETTER A WITH MACRON
        # U+0100 is LATIN CAPITAL LETTER A WITH MACRON
        assert convert(incoming, RUS, IAST_EXT, R, I) == out
        assert convert(out, IAST_EXT, RUS, I, R) == incoming


# ---------------------------------------------------------------------------
# Non-standard IAST look-alikes on input (issue #9)
#
# Many Gaudiya Vaiṣṇava song texts write the velar nasal ṅ (U+1E45) as the
# Polish-style ń (U+0144). It must be accepted as an input alias for ṅ, while
# the output stays canonical.
# ---------------------------------------------------------------------------


class TestIastInputAliases:
    def test_n_acute_alias_to_iast(self):
        # ń (U+0144) on input behaves exactly like ṅ (U+1E45)
        assert convert("sańge", IAST_EXT, IAST_EXT, I, I) == "sańge"  # same-encoding short-circuit
        assert convert("sańge", IAST_EXT, BALARAM_EXT, I, B) == convert("saṅge", IAST_EXT, BALARAM_EXT, I, B)

    def test_n_acute_alias_to_rus(self):
        assert convert("sańge", IAST_EXT, RUS, I, R) == "сан̇ге"

    def test_capital_n_acute_alias(self):
        assert convert("ŃA", IAST_EXT, RUS, I, R) == convert("ṄA", IAST_EXT, RUS, I, R)

    def test_full_verse_line(self):
        # "prabhu lokanātha kobe sańge loyā jābe" — no Latin ń must survive
        out = convert("prabhu lokanātha kobe sańge loyā jābe", IAST_EXT, RUS, I, R)
        assert "ń" not in out
        assert "сан̇ге" in out

    def test_alias_not_applied_for_non_iast_input(self):
        # A stray ń in non-IAST input is left untouched (не our alias's job)
        assert "ń" in convert("sańge", BALARAM_EXT, RUS, B, R)


# ---------------------------------------------------------------------------
# UKR_H — Ukrainian (кха) variant
#
# Identical to UKR_G (Ukrainian (кга)) except voiceless aspirated stops
# (kh, ch, .th, th, ph) render with х instead of г. Voiced aspirated stops
# (gh, jh, .dh, dh, bh) are unaffected and still render with г in both.
# ---------------------------------------------------------------------------


class TestUkrHRoundtrip:
    def test_iast_ext_to_ukr_h(self):
        expected = " ".join(UKR_H).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(IAST_EXT), IAST_EXT, UKR_H, I, UH) == expected

    def test_ukr_h_to_iast_ext(self):
        assert convert(full(UKR_H), UKR_H, IAST_EXT, UH, I) == full(IAST_EXT)

    def test_balaram_ext_to_ukr_h(self):
        expected = " ".join(UKR_H).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(BALARAM_EXT), BALARAM_EXT, UKR_H, B, UH) == expected

    def test_ukr_h_to_balaram_ext(self):
        assert convert(full(UKR_H), UKR_H, BALARAM_EXT, UH, B) == full(BALARAM_EXT)

    def test_velthuis_ext_to_ukr_h(self):
        expected = " ".join(UKR_H).replace("Дж ДЖ", "Дж Дж")
        assert convert(" ".join(VELTHUIS_EXT), VELTHUIS_EXT, UKR_H, V, UH) == expected

    def test_ukr_h_to_velthuis_ext(self):
        assert convert(full(UKR_H), UKR_H, VELTHUIS_EXT, UH, V) == full(VELTHUIS_EXT)

    def test_ukr_h_to_hk_ext(self):
        assert convert(full(UKR_H), UKR_H, HK_EXT, UH, H) == full(HK_EXT)

    # UKR_G and UKR_H share the same base alphabet table (the only difference
    # is aspirate post-processing), so this only shows up on an actual
    # consonant+h cluster, not on the bare alphabet tuple.
    @pytest.mark.parametrize(
        "ukr_g_word,ukr_h_word",
        [
            ("кга", "кха"),
            ("чга", "чха"),
            ("т̣га", "т̣ха"),
            ("тга", "тха"),
            ("пга", "пха"),
            ("ґга", "ґга"),
            ("джга", "джга"),
            ("д̣га", "д̣га"),
            ("дга", "дга"),
            ("бга", "бга"),
        ],
    )
    def test_ukr_g_to_ukr_h_aspirate_cluster(self, ukr_g_word, ukr_h_word):
        assert convert(ukr_g_word, UKR_G, UKR_H, UG, UH) == ukr_h_word

    @pytest.mark.parametrize(
        "ukr_h_word,ukr_g_word",
        [
            ("кха", "кга"),
            ("чха", "чга"),
            ("т̣ха", "т̣га"),
            ("тха", "тга"),
            ("пха", "пга"),
            ("ґга", "ґга"),
            ("джга", "джга"),
            ("д̣га", "д̣га"),
            ("дга", "дга"),
            ("бга", "бга"),
        ],
    )
    def test_ukr_h_to_ukr_g_aspirate_cluster(self, ukr_h_word, ukr_g_word):
        assert convert(ukr_h_word, UKR_H, UKR_G, UH, UG) == ukr_g_word

    def test_identity(self):
        assert convert(full(UKR_H), UKR_H, UKR_H, UH, UH) == full(UKR_H)


class TestAspirateSplit:
    """Only voiceless stops (kh, ch, .th, th, ph) differ between UKR_G and
    UKR_H; voiced stops (gh, jh, .dh, dh, bh) render with г in both."""

    @pytest.mark.parametrize(
        "iast_word,ukr_g_word,ukr_h_word",
        [
            ("kha", "кга", "кха"),
            ("cha", "чга", "чха"),
            ("ṭha", "т̣га", "т̣ха"),
            ("tha", "тга", "тха"),
            ("pha", "пга", "пха"),
        ],
    )
    def test_voiceless_aspirates_differ(self, iast_word, ukr_g_word, ukr_h_word):
        assert convert(iast_word, IAST_EXT, UKR_G, I, UG) == ukr_g_word
        assert convert(iast_word, IAST_EXT, UKR_H, I, UH) == ukr_h_word

    @pytest.mark.parametrize(
        "iast_word,ukr_word",
        [
            ("gha", "ґга"),
            ("jha", "джга"),
            ("ḍha", "д̣га"),
            ("dha", "дга"),
            ("bha", "бга"),
        ],
    )
    def test_voiced_aspirates_unchanged(self, iast_word, ukr_word):
        assert convert(iast_word, IAST_EXT, UKR_G, I, UG) == ukr_word
        assert convert(iast_word, IAST_EXT, UKR_H, I, UH) == ukr_word

    @pytest.mark.parametrize(
        "iast_word",
        ["kha", "cha", "ṭha", "tha", "pha", "gha", "jha", "ḍha", "dha", "bha"],
    )
    def test_roundtrip_through_ukr_g_and_ukr_h(self, iast_word):
        via_g = convert(convert(iast_word, IAST_EXT, UKR_G, I, UG), UKR_G, IAST_EXT, UG, I)
        via_h = convert(convert(iast_word, IAST_EXT, UKR_H, I, UH), UKR_H, IAST_EXT, UH, I)
        assert via_g == iast_word
        assert via_h == iast_word
