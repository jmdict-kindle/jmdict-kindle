#
# Copyright 2014, 2017 Jose Fonseca
# Copyright 2004, 2005 Choplair-network.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#


# See also:
# - http://en.wikipedia.org/wiki/Japanese_verb_conjugation
# - http://www.japaneseverbconjugator.com/


class InflectionError(Exception):
    pass


def _check(dict_form, pos, *suffixes):
    assert suffixes
    suffix_lens = [len(suffix) for suffix in suffixes]
    suffix_len = suffix_lens.pop()
    for l in suffix_lens:
        assert l == suffix_len

    suffix = dict_form[-suffix_len:]

    if suffix in suffixes:
        return

    msg = f"{dict_form}[{pos}] should end with {'/'.join(suffixes)}, but ends with {suffix}"

    raise InflectionError(msg)


def inflect(dict_form, pos):
    """That's here that we fully conjugate the verb from
    its dictionary form."""

    infl = {}

    if pos == "adj-i":
        _check(dict_form, pos, "い")

        radical = dict_form[:-1]

        infl["nominal"] = radical + "く"
        infl["past"] = radical + "かった"
        infl["negative"] = infl["nominal"] + "ない"
        infl["negative-polite"] = infl["nominal"] + "ありません"
        infl["participle"] = infl["nominal"] + "て"
        infl["provisional-conditional"] = radical + "ければ"
        infl["volitional"] = radical + "かろう"
        infl["noun"] = radical + "さ"

        return infl

    elif pos == "v1":
        # ichidan

        _check(dict_form, pos, "る")

        infl["nominal"] = dict_form[:-1]
        infl["past"] = infl["nominal"] + "た"
        infl["negative"] = infl["nominal"] + "ない"
        infl["participle"] = infl["nominal"] + "て"
        infl["potential"] = infl["nominal"] + "れる"
        infl["passive"] = infl["nominal"] + "られる"
        infl["causative"] = infl["nominal"] + "させる"
        infl["provisional-conditional"] = infl["nominal"] + "れば"
        infl["imperative"] = infl["nominal"] + "ろ"
        infl["volitional"] = infl["nominal"] + "よう"

    elif pos in ("v5b", "v5g", "v5k", "v5m", "v5n", "v5r", "v5s", "v5t", "v5u"):
        root = ""

        if pos == "v5t":
            _check(dict_form, pos, "つ")
            root = dict_form[:-1]
            infl["nominal"] = root + "ち"
            infl["past"] = root + "った"
            infl["negative"] = root + "たない"
            infl["participle"] = root + "って"
            infl["potential"] = root + "てる"
            infl["volitional"] = root + "とう"

        elif pos == "v5k":
            _check(dict_form, pos, "く")
            root = dict_form[:-1]
            infl["nominal"] = root + "き"
            infl["past"] = root + "いた"
            infl["negative"] = root + "かない"
            infl["participle"] = root + "いて"
            infl["potential"] = root + "ける"
            infl["volitional"] = root + "こう"

        elif pos == "v5g":
            _check(dict_form, pos, "ぐ")
            root = dict_form[:-1]
            infl["nominal"] = root + "ぎ"
            infl["past"] = root + "いだ"
            infl["negative"] = root + "がない"
            infl["participle"] = root + "いで"
            infl["potential"] = root + "げる"
            infl["volitional"] = root + "ごう"

        elif pos == "v5s":
            _check(dict_form, pos, "す")
            root = dict_form[:-1]
            infl["nominal"] = root + "し"
            infl["past"] = infl["nominal"] + "た"
            infl["negative"] = root + "さない"
            infl["participle"] = infl["nominal"] + "て"
            infl["potential"] = root + "せる"
            infl["volitional"] = root + "ぞう"

        elif pos == "v5n":
            _check(dict_form, pos, "ぬ")
            root = dict_form[:-1]
            infl["nominal"] = root + "に"
            infl["past"] = root + "んだ"
            infl["negative"] = root + "なない"
            infl["participle"] = root + "んで"
            infl["potential"] = root + "ねる"
            infl["volitional"] = root + "のう"

        elif pos == "v5b":
            _check(dict_form, pos, "ぶ")
            root = dict_form[:-1]
            infl["nominal"] = root + "び"
            infl["past"] = root + "んだ"
            infl["negative"] = root + "ばない"
            infl["participle"] = root + "んで"
            infl["potential"] = root + "べる"
            infl["volitional"] = root + "ぼう"

        elif pos == "v5m":
            _check(dict_form, pos, "む")
            root = dict_form[:-1]
            infl["nominal"] = root + "み"
            infl["past"] = root + "んだ"
            infl["negative"] = root + "まない"
            infl["participle"] = root + "んで"
            infl["potential"] = root + "める"
            infl["volitional"] = root + "もう"

        elif pos == "v5r":
            _check(dict_form, pos, "る")
            root = dict_form[:-1]
            infl["nominal"] = root + "り"
            infl["past"] = root + "った"
            infl["negative"] = root + "らない"
            infl["participle"] = root + "って"
            infl["potential"] = root + "れる"
            infl["volitional"] = root + "ろう"

        elif pos == "v5u":
            _check(dict_form, pos, "う")
            root = dict_form[:-1]
            infl["nominal"] = root + "い"
            infl["past"] = root + "った"
            infl["negative"] = root + "わない"
            infl["participle"] = root + "って"
            infl["potential"] = root + "える"
            infl["volitional"] = root + "おう"

        else:
            assert False
            # TODO: v5k-s
            # TODO: v5r-i
            # TODO: v5u-s
            # TODO: v5z

        _check(infl["negative"], "negative", "ない")
        infl["passive"] = infl["negative"][:-2] + "れる"
        infl["causative"] = infl["negative"][:-2] + "せる"

        _check(infl["potential"], "potential", "る")
        infl["provisional-conditional"] = infl["potential"][:-1] + "ば"
        infl["imperative"] = infl["potential"][:-1]

    elif pos == "vs-i":
        # suru

        _check(dict_form, pos, "為る", "する")

        if dict_form[-2] == "す":
            root = dict_form[:-2]
            infl["nominal"] = root + "し"
            infl["potential"] = root + "できる"
            infl["passive"] = root + "される"
            infl["causative"] = root + "させる"
            infl["provisional-conditional"] = root + "すれば"
            infl["imperative"] = root + "しろ"
            infl["volitional"] = root + "しよう"
        else:
            infl["nominal"] = dict_form[:-1]

        infl["past"] = infl["nominal"] + "た"
        infl["negative"] = infl["nominal"] + "ない"
        infl["participle"] = infl["nominal"] + "て"

    elif pos == "vk":
        # kuru

        _check(dict_form, pos, "来る", "來る", "くる")

        u_form = dict_form[:-1]
        if dict_form[-2] == "く":
            i_form = dict_form[:-2] + "き"
            o_form = dict_form[:-2] + "こ"
        else:
            i_form = dict_form[:-1]
            o_form = dict_form[:-1]

        infl["nominal"] = i_form
        infl["past"] = i_form + "た"
        infl["negative"] = o_form + "ない"
        infl["participle"] = i_form + "て"
        infl["potential"] = o_form + "れる"
        infl["passive"] = o_form + "られる"
        infl["causative"] = o_form + "させる"
        infl["provisional-conditional"] = u_form + "れば"
        infl["imperative"] = o_form + "い"
        infl["volitional"] = o_form + "よう"

    else:
        return infl

    nai_form = infl["negative"]
    assert nai_form[-2:] == "ない"
    infl["negative-nominal"] = nai_form[:-2] + "なく"
    infl["negative-past"] = nai_form[:-2] + "なかった"
    infl["negative-participle"] = nai_form[:-2] + "ないで"
    infl["negative-provisional-conditional"] = nai_form[:-2] + "なければ"
    infl["negative-provisional-conditional-colloquial"] = nai_form[:-2] + "なきゃ"

    infl["conditional"] = infl["past"] + "ら"

    infl["wish"] = infl["nominal"] + "たい"
    infl["wish-past"] = infl["nominal"] + "たかった"
    infl["wish-nominal"] = infl["nominal"] + "たく"

    infl["polite"] = infl["nominal"] + "ます"
    infl["past-polite"] = infl["nominal"] + "ました"
    infl["negative-polite"] = infl["nominal"] + "ません"
    infl["volitional-polite"] = infl["nominal"] + "ましょう"

    return infl
