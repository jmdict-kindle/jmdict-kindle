# vim: set fileencoding=utf-8 :

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

    msg = u"%s[%s] should end with %s, but ends with %s" % (
         dict_form,
         pos,
         u'/'.join(suffixes),
         suffix
    )

    raise InflectionError(msg)


def inflect(dict_form, pos):
    '''That's here that we fully conjugate the verb from
    its dictionary form.'''

    infl = {}

    if pos == 'adj-i':
        _check(dict_form, pos, u'い')

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

        _check(dict_form, pos, u'る')

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
            _check(dict_form, pos, u'つ')
            root = dict_form[:-1]
            infl['nominal'] = root + u'ち'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'たない'
            infl['participle'] = root + u'って'
            infl['potential'] = root + u'てる'
            infl['volitional'] = root + u'とう'

        elif pos == 'v5k':
            _check(dict_form, pos, u'く')
            root = dict_form[:-1]
            infl['nominal'] = root + u'き'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'かない'
            infl['participle'] = root + u'いて'
            infl['potential'] = root + u'ける'
            infl['volitional'] = root + u'こう'

        elif pos == 'v5g':
            _check(dict_form, pos, u'ぐ')
            root = dict_form[:-1]
            infl['nominal'] = root + u'ぎ'
            infl['past'] = root + u'いた'
            infl['negative'] = root + u'がない'
            infl['participle'] = root + u'いで'
            infl['potential'] = root + u'げる'
            infl['volitional'] = root + u'ごう'

        elif pos == 'v5s':
            _check(dict_form, pos, u'す')
            root = dict_form[:-1]
            infl['nominal'] = root + u'し'
            infl['past'] = infl['nominal'] + u'た'
            infl['negative'] = root + u'さない'
            infl['participle'] = infl['nominal'] + u'て'
            infl['potential'] = root + u'せる'
            infl['volitional'] = root + u'ぞう'

        elif pos == 'v5n':
            _check(dict_form, pos, u'ぬ')
            root = dict_form[:-1]
            infl['nominal'] = root + u'に'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'なない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'ねる'
            infl['volitional'] = root + u'のう'

        elif pos == 'v5b':
            _check(dict_form, pos, u'ぶ')
            root = dict_form[:-1]
            infl['nominal'] = root + u'び'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'ばない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'べる'
            infl['volitional'] = root + u'ぼう'

        elif pos == 'v5m':
            _check(dict_form, pos, u'む')
            root = dict_form[:-1]
            infl['nominal'] = root + u'み'
            infl['past'] = root + u'んだ'
            infl['negative'] = root + u'まない'
            infl['participle'] = root + u'んで'
            infl['potential'] = root + u'める'
            infl['volitional'] = root + u'もう'

        elif pos == 'v5r':
            _check(dict_form, pos, u'る')
            root = dict_form[:-1]
            infl['nominal'] = root + u'り'
            infl['past'] = root + u'った'
            infl['negative'] = root + u'らない'
            infl['participle'] = root + u'って'
            infl['potential'] = root + u'れる'
            infl['volitional'] = root + u'ろう'

        elif pos == 'v5u':
            _check(dict_form, pos, u'う')
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

        _check(infl['negative'], 'negative', u'ない')
        infl['passive'] = infl['negative'][:-2] + u'れる'
        infl['causative'] = infl['negative'][:-2] + u'せる'

        _check(infl['potential'], 'potential', u'る')
        infl['provisional-conditional'] = infl['potential'][:-1] + u'ば'
        infl['imperative'] = infl['potential'][:-1]

    elif pos == 'vs-i':
        # suru

        _check(dict_form, pos, u'為る', u'する')

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

        _check(dict_form, pos, u'来る', u'來る', u'くる')

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
