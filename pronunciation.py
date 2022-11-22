import csv
from html import escape
import sys

hiragana = (
    "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
    "あいうえおかきくけこさしすせそたちつてと"
    "なにぬねのはひふへほまみむめもやゆよらりるれろ"
    "わをんぁぃぅぇぉゃゅょっ"
)
katakana = (
    "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"
    "アイウエオカキクケコサシスセソタチツテト"
    "ナニヌネノハヒフヘホマミムメモヤユヨラリルレロ"
    "ワヲンァィゥェォャュョッ"
)
hiragana = [ord(char) for char in hiragana]
translate_table = dict(zip(hiragana, katakana))

HIGH_STATE = 0
LOW_STATE = 1


class Pronunciation:
    def __init__(self):
        self.dict = {}
        with open("./pronunciation/ACCDB_unicode.csv", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter=",")
            for row in csv_reader:
                self.dict[
                    f"{row['kanjiexpr']}-{row['midashigo'].translate(translate_table)}"
                ] = {
                    "nopronouncepos": row["nopronouncepos"],
                    "nasalsoundpos": row["nasalsoundpos"],
                    "ac": row["ac"],
                    "source": "ACCDB_unicode.csv",
                }

        with open("./pronunciation/accents.tsv", encoding="utf-8") as file:
            csv_reader = csv.DictReader(
                file, delimiter="\t", fieldnames=["kanjiexpr", "midashigo", "accent"]
            )
            for row in csv_reader:
                if row["midashigo"] == "":
                    row["midashigo"] = row[
                        "kanjiexpr"
                    ]  # if only kana then there is no midashigo

                accents = row["accent"].split(
                    ","
                )  # there can be multiple pronunciations per word

                # find best accent based on priority
                used_accent = ""
                priority = -1
                for accent in accents:
                    if (
                        "(" in accent
                    ):  # some accents contain info about when to use. Do not use elif since the same accen position can have multiple qualifiers
                        if "名" in accent and priority < 40:  # noun
                            priority = 40
                            used_accent = accent
                        if "副" in accent and priority < 35:  # adverb
                            priority = 35
                            used_accent = accent
                        if "代" in accent and priority < 30:  # pronoun
                            priority = 30
                            used_accent = accent
                        if "形動" in accent and priority < 10:  # adjectival noun
                            priority = 10
                            used_accent = accent
                        if "感" in accent and priority < 20:  # interjection
                            priority = 20
                            used_accent = accent
                        if not (
                            "名" in accent
                            or "副" in accent
                            or "代" in accent
                            or "形動" in accent
                            or "感" in accent
                        ):
                            raise Exception(f"unknown word type for: {accent}")
                    elif priority < 1:  # by default use first without qualifier
                        used_accent = accent
                        priority = 1

                if priority == -1:
                    raise Exception(
                        f"no accent selected for {row['kanjiexpr']} {row['midashigo']} {row['accent']}"
                    )

                # Turn accent position into notation used by ACCDB_unicode.csv
                accent_position_sound = int(
                    "".join((ch if ch in "0123456789" else "") for ch in used_accent)
                )  # get only number from string.
                falling_accent_position = accent_position_sound  # the accent position is per sound, but some sounds consist of two characters e.g. しゃ. That's why we need this distinction
                kana_count = len(row["midashigo"])
                if accent_position_sound > kana_count:
                    sys.stdout.write(
                        f"the accent position for {row['midashigo']} is greater than the string length ({accent_position_sound})\n"
                    )
                    continue
                # The accent position in the file looks at a word per sound, however some sounds consist of two kana e.g. しゃ
                # correct for that here
                i = 0
                sound_changer = "ぁぃぅぇぉゃゅょァィゥェォャュョ"  # っ isn't in there by design as it is considered a separate sound by accents.tsv.
                while i < falling_accent_position - 1:
                    if row["midashigo"][i] in sound_changer:
                        falling_accent_position += 1
                    i += 1
                if kana_count > falling_accent_position:
                    if (
                        row["midashigo"][falling_accent_position] in sound_changer
                        or row["midashigo"][falling_accent_position] == "ー"
                    ):  # if position after falling_accent_position is as small kana. Not +1 because array starts at 0
                        falling_accent_position += 1

                ac = ""
                # create actual pronunciation string

                # check if the first sound consist of 2 characters
                first_sound_character_count = 1
                if kana_count > 1:
                    if row["midashigo"][1] in sound_changer:
                        first_sound_character_count = 2

                # leading zeroes do not have to be included but can
                # for more details on pitch accent see https://en.wikipedia.org/wiki/Japanese_pitch_accent
                if accent_position_sound == 0:
                    ac = "".join(
                        "0" for i in range(1, first_sound_character_count + 1)
                    ) + "".join(
                        "1"
                        for i in range(first_sound_character_count + 1, kana_count + 1)
                    )
                elif accent_position_sound == 1:
                    ac = (
                        "".join("1" for i in range(1, first_sound_character_count))
                        + "2"
                        + "".join(
                            "0"
                            for i in range(
                                first_sound_character_count + 1, kana_count + 1
                            )
                        )
                    )
                else:
                    ac = (
                        "".join("0" for i in range(1, first_sound_character_count + 1))
                        + "".join(
                            "1"
                            for i in range(
                                first_sound_character_count + 1, falling_accent_position
                            )
                        )
                        + "2"
                        + "".join(
                            "0"
                            for i in range(falling_accent_position + 1, kana_count + 1)
                        )
                    )

                translation = row["midashigo"].translate(translate_table)
                if (
                    f"{row['kanjiexpr']}-{translation}" not in self.dict
                ):  # prefer accents.tsv data
                    self.dict[f"{row['kanjiexpr']}-{translation}"] = {
                        "nopronouncepos": None,
                        "nasalsoundpos": None,
                        "ac": ac,
                        "source": "accents.tsv",
                    }
                else:
                    self.dict[f"{row['kanjiexpr']}-{translation}"]["ac"] = ac
                    self.dict[f"{row['kanjiexpr']}-{translation}"][
                        "source"
                    ] = "accents.tsv"

    def addPronunciation(self, entries):
        count = 0
        for entry in entries:
            for reading in entry.readings:
                if reading.re_restr != None:
                    kanji = reading.re_restr
                elif len(entry.kanjis) > 0:
                    kanji = entry.kanjis[0].keb
                else:
                    kanji = reading.reb

                key = f"{kanji}-{reading.reb.translate(translate_table)}"
                if key in self.dict:
                    reading.pronunciation = self.dict[key]
                    count += 1
                else:
                    reading.pronunciation = None
        return count


def format_pronunciations(reading):
    """Format an entry from the data in the original database to something that uses html"""
    txt = reading.reb
    strlen = len(txt)
    if reading.pronunciation == None:
        return escape(txt, quote=False)

    acclen = len(reading.pronunciation["ac"])
    accent = "0" * (strlen - acclen) + reading.pronunciation["ac"]

    # Get the nasal positions
    nasal = []
    if reading.pronunciation["nasalsoundpos"]:
        positions = reading.pronunciation["nasalsoundpos"].split("0")
        for p in positions:
            if p:
                nasal.append(int(p))
            if not p:
                # e.g. "20" would result in ['2', '']
                nasal[-1] = nasal[-1] * 10

    # Get the no pronounce positions
    nopron = []
    if reading.pronunciation["nopronouncepos"]:
        positions = reading.pronunciation["nopronouncepos"].split("0")
        for p in positions:
            if p:
                nopron.append(int(p))
            if not p:
                # e.g. "20" would result in ['2', '']
                nopron[-1] = nopron[-1] * 10

    outstr = ""
    if int(accent[0]) > 0:
        state = HIGH_STATE
        outstr = outstr + '<span class="h">'
    else:
        state = LOW_STATE
        outstr = outstr + '<span class="l">'

    mora = []
    for i in range(strlen):
        a = int(accent[i])

        if state == HIGH_STATE:
            if a == 0:
                outstr = outstr + '</span><span class="l">'
                state = LOW_STATE
                mora.append(i + 1)
        else:
            if a > 0:
                outstr = outstr + '</span><span class="h">'
                state = HIGH_STATE

        outstr = outstr + escape(txt[i], quote=False)
        if (i + 1) in nopron:
            # outstr = outstr + "</span>" dont know what to do here
            outstr = outstr
        if (i + 1) in nasal:
            outstr = outstr + '<span class="nas">&#176;</span>'
        if a == 2:
            outstr = outstr + '</span><span class="l">&#42780;'
            state = LOW_STATE
            mora.append(i + 1)

    if len(mora) == 0:
        mora.append(0)
    separator = "; "
    outstr = outstr + f"</span> [{separator.join(str(x) for x in mora)}]"
    return outstr
