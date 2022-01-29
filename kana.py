#
# Copyright 2014 Jose Fonseca
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


# See http://en.wikipedia.org/wiki/Hiragana_(Unicode_block)
_hiragana_xtab = dict([(_c, None) for _c in range(0x3041, 0x3097)])


def is_hiragana(word):
    assert isinstance(word, str)
    return word.translate(_hiragana_xtab) == ""


# See http://en.wikipedia.org/wiki/Katakana_(Unicode_block)
_katakana_xtab = dict([(_c, None) for _c in range(0x30A1, 0x30FD)])


def is_katakana(word):
    assert isinstance(word, str)
    return word.translate(_katakana_xtab) == ""


_kana_xtab = {}
_kana_xtab.update(_hiragana_xtab)
_kana_xtab.update(_katakana_xtab)


def is_kana(word):
    assert isinstance(word, str)
    return word.translate(_kana_xtab) == ""
