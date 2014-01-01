# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

#
# Copyright 2014 Jose Fonseca
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


def is_katakana(word):
    assert isinstance(word, unicode)
    for c in word:
        ord_c = ord(c)
        if ord_c < 12449 or ord_c >= 12534:
            return False
    return True
    

def inflect(dict_form, pos):
    '''That's here that we fully conjugate the verb from
    its dictionary form.'''

    infl = {}

    if pos == 'adj-i':
        assert dict_form[-1] == u'い'

        radical = dict_form[:-1]

        infl['nominal'] = radical + u'く'
        infl['past'] = radical + u'かった'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['negative-polite'] = infl['nominal'] + u'ありません'
        infl['participle'] = infl['nominal'] + u'て'
        infl['provisional-conditional'] = radical + u'ければ'

        return infl

    elif pos == 'v1':
        # ichidan

        assert dict_form[-1:] == u'る'

        infl['nominal'] = dict_form[:-1]
        infl['past'] = infl['nominal'] + u'た'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['participle'] = infl['nominal'] + u'て'
        infl['potential'] = infl['nominal'] + u'られる'
        infl['causative'] = infl['nominal'] + u'させる'
        infl['provisional-conditional'] = infl['nominal'] + u'れば'
        infl['volitional'] = infl['nominal'] + u'よう'

    elif pos in ('v5b', 'v5g', 'v5k', 'v5m', 'v5n', 'v5r', 'v5s', 'v5t', 'v5u'):
        root = ''

        if pos == 'v5t':
            assert dict_form[-1:] == u'つ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'ち'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'たない'
            infl['participle'] = root + u'って'
            infl['provisional-conditional'] = infl['nominal'] + u'てば'

        elif pos == 'v5k':
            assert dict_form[-1:] == u'く'
            root = dict_form[:-1]
            infl['nominal'] = root + u'き'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'かない'
            infl['participle'] = root + u'いて'
            infl['provisional-conditional'] = infl['nominal'] + u'けば'

        elif pos == 'v5g':
            assert dict_form[-1:] == u'ぐ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'ぎ'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'がない'
            infl['participle'] = root + u'いで'
            infl['provisional-conditional'] = infl['nominal'] + u'げば'

        elif pos == 'v5s':
            assert dict_form[-1:] == u'す'
            root = dict_form[:-1]
            infl['nominal'] = root + u'し'
            infl['past'] = infl['nominal'] + u'た'
            infl['negative'] = root + u'さない'
            infl['participle'] = infl['nominal'] + u'て'
            infl['provisional-conditional'] = infl['nominal'] + u'せば'

        elif pos == 'v5n':
            assert dict_form[-1:] == u'ぬ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'に'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'なない'
            infl['participle'] = root + u'んで'
            infl['provisional-conditional'] = infl['nominal'] + u'ねば'

        elif pos == 'v5b':
            assert dict_form[-1:] == u'ぶ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'び'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'ばない'
            infl['participle'] = root + u'んで'
            infl['provisional-conditional'] = infl['nominal'] + u'べば'

        elif pos == 'v5m':
            assert dict_form[-1:] == u'む'
            root = dict_form[:-1]
            infl['nominal'] = root + u'み'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'まない'
            infl['participle'] = root + u'んで'
            infl['provisional-conditional'] = infl['nominal'] + u'めば'

        elif pos == 'v5r':
            assert dict_form[-1:] == u'る'
            root = dict_form[:-1]
            infl['nominal'] = root + u'り'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'らない'
            infl['participle'] = root + u'って'
            infl['provisional-conditional'] = infl['nominal'] + u'れば'

        elif pos == 'v5u':
            assert dict_form[-1:] == u'う'
            root = dict_form[:-1]
            infl['nominal'] = root + u'い'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'わない'
            infl['participle'] = root + u'って'
            infl['provisional-conditional'] = infl['nominal'] + u'えば'

        else:
            assert False
            # TODO: v5k-s
            # TODO: v5r-i
            # TODO: v5u-s
            # TODO: v5z

        infl['causative'] = infl['negative'][:-2] + u'せる'
        infl['volitional'] = infl['nominal'] + u'よう'

    elif pos == 'vs-i':
        # suru

        assert dict_form[-1] == u'る'
        assert dict_form[-2] in u'為す'

        if dict_form[-2] == u'す':
            infl['nominal'] = dict_form[:-2] + u'し'
            infl['causative'] = dict_form[:-2] + u'させる'
        else:
            infl['nominal'] = dict_form[:-1]
            # infl['causative'] = ???

        infl['past'] = infl['nominal'] + u'た'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['participle'] = infl['nominal'] + u'て'
        # infl['potential'] = ???
        infl['provisional-conditional'] = infl['nominal'] + u'れば'
        infl['volitional'] = infl['nominal'] + u'よう'

    elif pos == 'vk':
        # kuru

        assert dict_form[-1] == u'る'
        assert dict_form[-2] in u'来來く'
        
        if dict_form[-2] == u'く':
            infl['nominal'] = dict_form[:-2] + u'き'
            infl['potential'] = dict_form[:-2] + u'こられる'
        else:
            infl['nominal'] = dict_form[:-1]
            infl['potential'] = infl['nominal'] + u'られる'

        infl['past'] = infl['nominal'] + u'た'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['participle'] = infl['nominal'] + u'て'
        infl['causative'] = infl['potential'][:-3] + u'させる'
        infl['provisional-conditional'] = infl['nominal'] + u'れば'
        infl['volitional'] = infl['nominal'] + u'よう'

    else:
        return infl

    nai_form = infl['negative']
    assert nai_form[-2:] == u'ない'
    infl['past-negative'] = nai_form[:-2] + u'なかった'
    infl['participle-negative'] = nai_form[:-2] + u'ないで'

    infl['polite'] = infl['nominal'] + u'ます'
    infl['past-polite'] = infl['nominal'] + u'ました'
    infl['negative-polite'] = infl['nominal'] + u'ません'
    infl['volitional-polite'] = infl['nominal'] + u'ましょう'

    return infl
