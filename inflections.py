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
        infl['volitional'] = radical + u'かろう'

        return infl

    elif pos == 'v1':
        # ichidan

        assert dict_form[-1:] == u'る'

        infl['nominal'] = dict_form[:-1]
        infl['past'] = infl['nominal'] + u'た'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['participle'] = infl['nominal'] + u'て'
        infl['potential'] = infl['nominal'] + u'れる'
        infl['passive'] = infl['nominal'] + u'られる'
        infl['causative'] = infl['nominal'] + u'させる'
        infl['provisional-conditional'] = infl['nominal'] + u'れば'
        infl['imperative'] = infl['nominal'] + u'ろ'
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
            infl['potential'] = root + u'てる'
            infl['volitional'] = root + u'とう'

        elif pos == 'v5k':
            assert dict_form[-1:] == u'く'
            root = dict_form[:-1]
            infl['nominal'] = root + u'き'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'かない'
            infl['participle'] = root + u'いて'
            infl['potential'] = root + u'ける'
            infl['volitional'] = root + u'こう'

        elif pos == 'v5g':
            assert dict_form[-1:] == u'ぐ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'ぎ'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'がない'
            infl['participle'] = root + u'いで'
            infl['potential'] = root + u'げる'
            infl['volitional'] = root + u'ごう'

        elif pos == 'v5s':
            assert dict_form[-1:] == u'す'
            root = dict_form[:-1]
            infl['nominal'] = root + u'し'
            infl['past'] = infl['nominal'] + u'た'
            infl['negative'] = root + u'さない'
            infl['participle'] = infl['nominal'] + u'て'
            infl['potential'] = root + u'せる'
            infl['volitional'] = root + u'ぞう'

        elif pos == 'v5n':
            assert dict_form[-1:] == u'ぬ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'に'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'なない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'ねる'
            infl['volitional'] = root + u'のう'

        elif pos == 'v5b':
            assert dict_form[-1:] == u'ぶ'
            root = dict_form[:-1]
            infl['nominal'] = root + u'び'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'ばない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'べる'
            infl['volitional'] = root + u'ぼう'

        elif pos == 'v5m':
            assert dict_form[-1:] == u'む'
            root = dict_form[:-1]
            infl['nominal'] = root + u'み'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'まない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'める'
            infl['volitional'] = root + u'もう'

        elif pos == 'v5r':
            assert dict_form[-1:] == u'る'
            root = dict_form[:-1]
            infl['nominal'] = root + u'り'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'らない'
            infl['participle'] = root + u'って'
            infl['potential'] = root + u'れる'
            infl['volitional'] = root + u'ろう'

        elif pos == 'v5u':
            assert dict_form[-1:] == u'う'
            root = dict_form[:-1]
            infl['nominal'] = root + u'い'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'わない'
            infl['participle'] = root + u'って'
            infl['potential'] = root + u'える'
            infl['volitional'] = root + u'おう'

        else:
            assert False
            # TODO: v5k-s
            # TODO: v5r-i
            # TODO: v5u-s
            # TODO: v5z

        assert infl['negative'][-2:] == u'ない'
        infl['passive'] = infl['negative'][:-2] + u'れる'
        infl['causative'] = infl['negative'][:-2] + u'せる'

        assert infl['potential'][-1:] == u'る'
        infl['provisional-conditional'] = infl['potential'][:-1] + u'ば'
        infl['imperative'] = infl['potential'][:-1]

    elif pos == 'vs-i':
        # suru

        assert dict_form[-1] == u'る'
        assert dict_form[-2] in u'為す'

        if dict_form[-2] == u'す':
            root = dict_form[:-2]
            infl['nominal'] = root + u'し'
            infl['potential'] = root + u'できる'
            infl['passive'] = root + u'される'
            infl['causative'] = root + u'させる'
            infl['provisional-conditional'] = root + u'すれば'
            infl['imperative'] = root + u'しろ'
            infl['volitional'] = root + u'しよう'
        else:
            infl['nominal'] = dict_form[:-1]

        infl['past'] = infl['nominal'] + u'た'
        infl['negative'] = infl['nominal'] + u'ない'
        infl['participle'] = infl['nominal'] + u'て'

    elif pos == 'vk':
        # kuru

        assert dict_form[-1] == u'る'
        assert dict_form[-2] in u'来來く'
        
        u_form = dict_form[:-1]
        if dict_form[-2] == u'く':
            i_form = dict_form[:-2] + u'き'
            o_form = dict_form[:-2] + u'こ'
        else:
            i_form = dict_form[:-1]
            o_form = dict_form[:-1]

        infl['nominal'] = i_form
        infl['past'] = i_form + u'た'
        infl['negative'] = o_form + u'ない'
        infl['participle'] = i_form + u'て'
        infl['potential'] = o_form + u'れる'
        infl['passive'] = o_form + u'られる'
        infl['causative'] = o_form + u'させる'
        infl['provisional-conditional'] = u_form + u'れば'
        infl['imperative'] = o_form + u'い'
        infl['volitional'] = o_form + u'よう'

    else:
        return infl

    nai_form = infl['negative']
    assert nai_form[-2:] == u'ない'
    infl['negative-nominal'] = nai_form[:-2] + u'なく'
    infl['negative-past'] = nai_form[:-2] + u'なかった'
    infl['negative-participle'] = nai_form[:-2] + u'ないで'
    infl['negative-provisional-conditional'] = nai_form[:-2] + u'なければ'
    infl['negative-provisional-conditional-colloquial'] = nai_form[:-2] + u'なきゃ'

    infl['conditional'] = infl['past'] + u'ら'

    infl['wish'] = infl['nominal'] + u'たい'
    infl['wish-past'] = infl['nominal'] + u'たかった'
    infl['wish-nominal'] = infl['nominal'] + u'たく'

    infl['polite'] = infl['nominal'] + u'ます'
    infl['past-polite'] = infl['nominal'] + u'ました'
    infl['negative-polite'] = infl['nominal'] + u'ません'
    infl['volitional-polite'] = infl['nominal'] + u'ましょう'

    return infl
